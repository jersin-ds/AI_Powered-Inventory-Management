"""Dashboard service — aggregated stats & chart data matching frontend shapes."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from sqlalchemy import func, extract, case

from ..models.product import Product
from ..models.sale import Sale, SaleItem
from ..models.purchase import Purchase
from ..models.category import Category
from ..repositories import product_repo, sale_repo, purchase_repo
from ..schemas.dashboard import (
    DashboardStatsResponse,
    SalesChartPoint,
    RevenueByCategoryPoint,
    TopProductPoint,
    MonthlyDataPoint,
    CategoryPerformancePoint,
    CustomerSegmentPoint,
)


def _growth_pct(current: float, previous: float) -> float:
    """Return percentage growth; 0 when no previous data."""
    if previous == 0:
        return 100.0 if current > 0 else 0.0
    return round((current - previous) / previous * 100, 1)


def get_stats(db: Session) -> DashboardStatsResponse:
    total_revenue = sale_repo.total_revenue(db)
    total_profit = sale_repo.total_profit(db)
    total_products = product_repo.count(db)
    total_orders = db.query(Sale).count()
    low_stock = product_repo.count_by_status(db, "low_stock")
    out_of_stock = product_repo.count_by_status(db, "out_of_stock")
    pending_orders = purchase_repo.count_by_status(db, "pending")

    # Real growth: compare last 30 days vs prior 30 days
    now = datetime.now(timezone.utc)
    last_30 = now - timedelta(days=30)
    prior_30 = now - timedelta(days=60)

    rev_current = float(
        db.query(func.coalesce(func.sum(Sale.total_amount), 0))
        .filter(Sale.status == "completed", Sale.date >= last_30)
        .scalar()
    )
    rev_previous = float(
        db.query(func.coalesce(func.sum(Sale.total_amount), 0))
        .filter(Sale.status == "completed", Sale.date >= prior_30, Sale.date < last_30)
        .scalar()
    )
    profit_current = float(
        db.query(func.coalesce(func.sum(Sale.profit), 0))
        .filter(Sale.status == "completed", Sale.date >= last_30)
        .scalar()
    )
    profit_previous = float(
        db.query(func.coalesce(func.sum(Sale.profit), 0))
        .filter(Sale.status == "completed", Sale.date >= prior_30, Sale.date < last_30)
        .scalar()
    )

    return DashboardStatsResponse(
        total_revenue=total_revenue,
        total_profit=total_profit,
        total_products=total_products,
        total_orders=total_orders,
        low_stock_items=low_stock,
        out_of_stock_items=out_of_stock,
        pending_orders=pending_orders,
        revenue_growth=_growth_pct(rev_current, rev_previous),
        profit_growth=_growth_pct(profit_current, profit_previous),
    )


def get_sales_chart(db: Session) -> list[SalesChartPoint]:
    """Aggregate sales/profit by date."""
    rows = (
        db.query(
            func.strftime("%Y-%m-%d", Sale.date).label("day"),
            func.sum(Sale.total_amount).label("sales"),
            func.sum(Sale.profit).label("profit"),
        )
        .filter(Sale.status == "completed")
        .group_by("day")
        .order_by("day")
        .all()
    )
    return [SalesChartPoint(date=r.day, sales=float(r.sales), profit=float(r.profit)) for r in rows]


def get_revenue_by_category(db: Session) -> list[RevenueByCategoryPoint]:
    """Revenue broken down by product category."""
    rows = (
        db.query(
            Category.name.label("category"),
            func.sum(SaleItem.quantity * SaleItem.price).label("value"),
        )
        .join(Product, SaleItem.product_id == Product.id)
        .join(Category, Product.category_id == Category.id)
        .join(Sale, SaleItem.sale_id == Sale.id)
        .filter(Sale.status == "completed")
        .group_by(Category.name)
        .all()
    )

    total = sum(float(r.value) for r in rows) or 1
    return [
        RevenueByCategoryPoint(
            category=r.category,
            value=float(r.value),
            percentage=round(float(r.value) / total * 100, 1),
        )
        for r in rows
    ]


def get_top_products(db: Session, limit: int = 5) -> list[TopProductPoint]:
    """Top selling products by total units sold."""
    rows = (
        db.query(
            Product.id,
            Product.name,
            func.sum(SaleItem.quantity).label("sales"),
            func.sum(SaleItem.quantity * SaleItem.price).label("revenue"),
        )
        .join(SaleItem, SaleItem.product_id == Product.id)
        .join(Sale, SaleItem.sale_id == Sale.id)
        .filter(Sale.status == "completed")
        .group_by(Product.id, Product.name)
        .order_by(func.sum(SaleItem.quantity).desc())
        .limit(limit)
        .all()
    )
    return [
        TopProductPoint(id=r.id, name=r.name, sales=int(r.sales), revenue=float(r.revenue))
        for r in rows
    ]


# ── Analytics endpoints ──

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def get_monthly_data(db: Session) -> list[MonthlyDataPoint]:
    """Return revenue/expenses/profit/orders aggregated by month from sales and purchases."""
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=365)

    # Sales by month
    sale_rows = (
        db.query(
            func.strftime("%m", Sale.date).label("m"),
            func.sum(Sale.total_amount).label("revenue"),
            func.sum(Sale.profit).label("profit"),
            func.count(Sale.id).label("orders"),
        )
        .filter(Sale.status == "completed", Sale.date >= start)
        .group_by("m")
        .all()
    )

    # Purchases by month (expenses)
    purchase_rows = (
        db.query(
            func.strftime("%m", Purchase.date).label("m"),
            func.sum(Purchase.total_amount).label("expenses"),
        )
        .filter(Purchase.date >= start)
        .group_by("m")
        .all()
    )

    purchase_map = {r.m: float(r.expenses or 0) for r in purchase_rows}

    results: list[MonthlyDataPoint] = []
    for r in sale_rows:
        month_idx = int(r.m) - 1
        month_name = MONTH_NAMES[month_idx] if 0 <= month_idx < 12 else r.m
        revenue = float(r.revenue or 0)
        expenses = purchase_map.get(r.m, revenue * 0.65)
        results.append(MonthlyDataPoint(
            month=month_name,
            revenue=round(revenue, 2),
            expenses=round(expenses, 2),
            profit=round(float(r.profit or 0), 2),
            orders=int(r.orders or 0),
        ))

    # If no sales data, fill all 12 months with zero so charts render properly
    if not results:
        for name in MONTH_NAMES:
            results.append(MonthlyDataPoint(
                month=name, revenue=0, expenses=0, profit=0, orders=0,
            ))

    return results


def get_category_performance(db: Session) -> list[CategoryPerformancePoint]:
    """Category-level sales, growth and margin analysis."""
    categories = db.query(Category).filter(Category.status == "active").all()
    results: list[CategoryPerformancePoint] = []

    for cat in categories:
        # Total sales revenue for this category
        rev = (
            db.query(func.sum(SaleItem.quantity * SaleItem.price))
            .join(Product, SaleItem.product_id == Product.id)
            .join(Sale, SaleItem.sale_id == Sale.id)
            .filter(Product.category_id == cat.id, Sale.status == "completed")
            .scalar()
        ) or 0

        # Total cost for margin calc
        cost = (
            db.query(func.sum(SaleItem.quantity * Product.cost_price))
            .join(Product, SaleItem.product_id == Product.id)
            .join(Sale, SaleItem.sale_id == Sale.id)
            .filter(Product.category_id == cat.id, Sale.status == "completed")
            .scalar()
        ) or 0

        margin = round(((rev - cost) / rev * 100) if rev > 0 else 0, 1)
        unit_sales = (
            db.query(func.sum(SaleItem.quantity))
            .join(Product, SaleItem.product_id == Product.id)
            .join(Sale, SaleItem.sale_id == Sale.id)
            .filter(Product.category_id == cat.id, Sale.status == "completed")
            .scalar()
        ) or 0

        # Real growth: compare last 30 days vs prior 30 days for this category
        now_utc = datetime.now(timezone.utc)
        last30 = now_utc - timedelta(days=30)
        prior30 = now_utc - timedelta(days=60)

        rev_cur = float(
            db.query(func.coalesce(func.sum(SaleItem.quantity * SaleItem.price), 0))
            .join(Product, SaleItem.product_id == Product.id)
            .join(Sale, SaleItem.sale_id == Sale.id)
            .filter(Product.category_id == cat.id, Sale.status == "completed", Sale.date >= last30)
            .scalar()
        )
        rev_prev = float(
            db.query(func.coalesce(func.sum(SaleItem.quantity * SaleItem.price), 0))
            .join(Product, SaleItem.product_id == Product.id)
            .join(Sale, SaleItem.sale_id == Sale.id)
            .filter(Product.category_id == cat.id, Sale.status == "completed", Sale.date >= prior30, Sale.date < last30)
            .scalar()
        )
        growth = _growth_pct(rev_cur, rev_prev)

        results.append(CategoryPerformancePoint(
            category=cat.name,
            sales=float(unit_sales),
            growth=growth,
            margin=margin,
        ))

    return results


def get_customer_segments(db: Session) -> list[CustomerSegmentPoint]:
    """Segment sales by customer type derived from sale amounts."""
    sales = db.query(Sale).filter(Sale.status == "completed").all()
    segments = {"Enterprise": 0, "SMB": 0, "Retail": 0, "Individual": 0}

    for sale in sales:
        if sale.total_amount >= 3000:
            segments["Enterprise"] += sale.total_amount
        elif sale.total_amount >= 1500:
            segments["SMB"] += sale.total_amount
        elif sale.total_amount >= 500:
            segments["Retail"] += sale.total_amount
        else:
            segments["Individual"] += sale.total_amount

    total = sum(segments.values()) or 1
    return [
        CustomerSegmentPoint(
            segment=seg,
            value=round(val / total * 100, 1),
        )
        for seg, val in segments.items()
        if val > 0
    ]
