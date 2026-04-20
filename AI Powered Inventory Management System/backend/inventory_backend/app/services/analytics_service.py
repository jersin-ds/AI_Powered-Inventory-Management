"""Analytics service — monthly aggregation, category performance, segments."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from ..models.sale import Sale, SaleItem
from ..models.purchase import Purchase
from ..models.product import Product
from ..models.category import Category
from ..schemas.dashboard import (
    MonthlyDataPoint,
    CategoryPerformancePoint,
    CustomerSegmentPoint,
)


def _growth_pct(current: float, previous: float) -> float:
    """Return percentage growth; 0 when no previous data."""
    if previous == 0:
        return 100.0 if current > 0 else 0.0
    return round((current - previous) / previous * 100, 1)


def get_monthly_data(db: Session) -> list[MonthlyDataPoint]:
    """Monthly revenue, expenses, profit, orders."""
    # Revenue & profit from sales
    sales_rows = (
        db.query(
            func.strftime("%Y-%m", Sale.date).label("month"),
            func.sum(Sale.total_amount).label("revenue"),
            func.sum(Sale.profit).label("profit"),
            func.count(Sale.id).label("orders"),
        )
        .filter(Sale.status == "completed")
        .group_by("month")
        .order_by("month")
        .all()
    )

    # Expenses from purchases
    purchase_rows = (
        db.query(
            func.strftime("%Y-%m", Purchase.date).label("month"),
            func.sum(Purchase.total_amount).label("expenses"),
        )
        .filter(Purchase.status.in_(["received", "pending"]))
        .group_by("month")
        .all()
    )
    expense_map = {r.month: float(r.expenses) for r in purchase_rows}

    months_map = {
        "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
        "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
        "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec",
    }

    results = []
    for r in sales_rows:
        month_str = r.month  # e.g. "2024-02"
        month_label = months_map.get(month_str[-2:], month_str[-2:]) if month_str else "?"
        expenses = expense_map.get(month_str, 0)
        results.append(
            MonthlyDataPoint(
                month=month_label,
                revenue=float(r.revenue),
                expenses=expenses,
                profit=float(r.profit),
                orders=int(r.orders),
            )
        )

    return results


def get_category_performance(db: Session) -> list[CategoryPerformancePoint]:
    """Sales, real growth (30-day vs prior 30-day), and real margin by category."""
    now = datetime.now(timezone.utc)
    last_30 = now - timedelta(days=30)
    prior_30 = now - timedelta(days=60)

    # Current period sales per category
    current_rows = (
        db.query(
            Category.name.label("category"),
            func.sum(SaleItem.quantity * SaleItem.price).label("revenue"),
            func.sum(SaleItem.quantity * Product.cost_price).label("cost"),
        )
        .join(Product, SaleItem.product_id == Product.id)
        .join(Category, Product.category_id == Category.id)
        .join(Sale, SaleItem.sale_id == Sale.id)
        .filter(Sale.status == "completed", Sale.date >= last_30)
        .group_by(Category.name)
        .all()
    )

    # Prior period sales per category (for growth calculation)
    prior_rows = (
        db.query(
            Category.name.label("category"),
            func.sum(SaleItem.quantity * SaleItem.price).label("revenue"),
        )
        .join(Product, SaleItem.product_id == Product.id)
        .join(Category, Product.category_id == Category.id)
        .join(Sale, SaleItem.sale_id == Sale.id)
        .filter(Sale.status == "completed", Sale.date >= prior_30, Sale.date < last_30)
        .group_by(Category.name)
        .all()
    )
    prior_map = {r.category: float(r.revenue) for r in prior_rows}

    # All-time totals for overall sales value
    all_time_rows = (
        db.query(
            Category.name.label("category"),
            func.sum(SaleItem.quantity * SaleItem.price).label("sales"),
            func.sum(SaleItem.quantity * Product.cost_price).label("cost"),
        )
        .join(Product, SaleItem.product_id == Product.id)
        .join(Category, Product.category_id == Category.id)
        .join(Sale, SaleItem.sale_id == Sale.id)
        .filter(Sale.status == "completed")
        .group_by(Category.name)
        .all()
    )
    all_time_map = {r.category: (float(r.sales), float(r.cost)) for r in all_time_rows}

    # Build current-period lookup
    current_map = {r.category: (float(r.revenue), float(r.cost)) for r in current_rows}

    results = []
    # Use all-time categories so every category appears
    for cat, (total_sales, total_cost) in all_time_map.items():
        cur_rev = current_map.get(cat, (0, 0))[0]
        prev_rev = prior_map.get(cat, 0)
        growth = _growth_pct(cur_rev, prev_rev)
        margin = round((total_sales - total_cost) / total_sales * 100, 1) if total_sales > 0 else 0.0
        results.append(
            CategoryPerformancePoint(
                category=cat,
                sales=total_sales,
                growth=growth,
                margin=margin,
            )
        )
    return results


def get_customer_segments(db: Session) -> list[CustomerSegmentPoint]:
    """Segment customers by total purchase value."""
    rows = (
        db.query(
            Sale.customer.label("segment"),
            func.sum(Sale.total_amount).label("value"),
        )
        .filter(Sale.status == "completed")
        .group_by(Sale.customer)
        .order_by(func.sum(Sale.total_amount).desc())
        .all()
    )
    return [CustomerSegmentPoint(segment=r.segment, value=float(r.value)) for r in rows]
