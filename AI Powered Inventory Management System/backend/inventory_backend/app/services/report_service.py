"""Report service — generate report data matching frontend expectations."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.sale import Sale
from ..models.purchase import Purchase
from ..models.product import Product
from ..models.category import Category
from ..repositories import sale_repo, purchase_repo, product_repo
from ..schemas.dashboard import ReportSummary
from ..schemas.sale import SaleResponse, SaleItemSchema
from ..schemas.purchase import PurchaseResponse, PurchaseItemSchema
from ..schemas.product import ProductResponse
from ..services.product_service import _to_response as product_to_response


def _get_date_range(range_str: str) -> datetime:
    """Return start datetime from range string."""
    now = datetime.now(timezone.utc)
    mapping = {
        "7days": timedelta(days=7),
        "30days": timedelta(days=30),
        "90days": timedelta(days=90),
        "year": timedelta(days=365),
    }
    delta = mapping.get(range_str, timedelta(days=30))
    return now - delta


def sales_report(db: Session, date_range: str = "30days") -> ReportSummary:
    start = _get_date_range(date_range)
    sales = (
        db.query(Sale)
        .filter(Sale.date >= start)
        .order_by(Sale.date.desc())
        .all()
    )

    total_sales = sum(s.total_amount for s in sales if s.status == "completed")
    total_profit = sum(s.profit for s in sales if s.status == "completed")
    total_orders = len(sales)
    avg_order = total_sales / total_orders if total_orders > 0 else 0

    return ReportSummary(
        title="Sales Report",
        period=date_range,
        summary={
            "totalSales": round(total_sales, 2),
            "totalOrders": total_orders,
            "avgOrderValue": round(avg_order, 2),
            "totalProfit": round(total_profit, 2),
        },
        data=[
            {
                "id": s.id,
                "invoiceNumber": s.invoice_number,
                "customer": s.customer,
                "date": str(s.date)[:10],
                "status": s.status,
                "totalAmount": s.total_amount,
                "profit": s.profit,
            }
            for s in sales
        ],
    )


def purchases_report(db: Session, date_range: str = "30days") -> ReportSummary:
    start = _get_date_range(date_range)
    purchases = (
        db.query(Purchase)
        .filter(Purchase.date >= start)
        .order_by(Purchase.date.desc())
        .all()
    )

    total_purchases = sum(p.total_amount for p in purchases)
    total_orders = len(purchases)
    avg_order = total_purchases / total_orders if total_orders > 0 else 0
    pending = sum(1 for p in purchases if p.status == "pending")

    return ReportSummary(
        title="Purchases Report",
        period=date_range,
        summary={
            "totalPurchases": round(total_purchases, 2),
            "totalOrders": total_orders,
            "avgOrderValue": round(avg_order, 2),
            "pendingOrders": pending,
        },
        data=[
            {
                "id": p.id,
                "poNumber": p.po_number,
                "supplier": p.supplier_name,
                "date": str(p.date)[:10],
                "status": p.status,
                "totalAmount": p.total_amount,
            }
            for p in purchases
        ],
    )


def inventory_report(db: Session, date_range: str = "30days") -> ReportSummary:
    products = product_repo.get_all(db)
    total_value = sum(p.stock_qty * p.cost_price for p in products)
    low_stock = sum(1 for p in products if p.status == "low_stock")
    out_of_stock = sum(1 for p in products if p.status == "out_of_stock")

    # Pre-load category names
    cat_map = {c.id: c.name for c in db.query(Category).all()}

    return ReportSummary(
        title="Inventory Report",
        period=date_range,
        summary={
            "totalProducts": len(products),
            "totalValue": round(total_value, 2),
            "lowStock": low_stock,
            "outOfStock": out_of_stock,
        },
        data=[
            {
                "id": p.id,
                "name": p.name,
                "sku": p.sku,
                "category": cat_map.get(p.category_id, "Uncategorized"),
                "costPrice": p.cost_price,
                "stockQty": p.stock_qty,
                "minLevel": p.min_level,
                "status": p.status,
                "value": round(p.stock_qty * p.cost_price, 2),
            }
            for p in products
        ],
    )


def profit_report(db: Session, date_range: str = "30days") -> ReportSummary:
    start = _get_date_range(date_range)
    now = datetime.now(timezone.utc)

    total_revenue = float(
        db.query(func.coalesce(func.sum(Sale.total_amount), 0))
        .filter(Sale.status == "completed", Sale.date >= start)
        .scalar()
    )
    total_profit = float(
        db.query(func.coalesce(func.sum(Sale.profit), 0))
        .filter(Sale.status == "completed", Sale.date >= start)
        .scalar()
    )

    # Growth: compare this period vs same-length prior period
    period_len = now - start
    prior_start = start - period_len
    prev_profit = float(
        db.query(func.coalesce(func.sum(Sale.profit), 0))
        .filter(Sale.status == "completed", Sale.date >= prior_start, Sale.date < start)
        .scalar()
    )
    if prev_profit > 0:
        growth = round((total_profit - prev_profit) / prev_profit * 100, 1)
    else:
        growth = 100.0 if total_profit > 0 else 0.0

    margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0

    # Date-level profit breakdown
    rows = (
        db.query(
            func.strftime("%Y-%m-%d", Sale.date).label("day"),
            func.sum(Sale.total_amount).label("revenue"),
            func.sum(Sale.profit).label("profit"),
            func.count(Sale.id).label("orders"),
        )
        .filter(Sale.status == "completed", Sale.date >= start)
        .group_by("day")
        .order_by("day")
        .all()
    )

    return ReportSummary(
        title="Profit Report",
        period=date_range,
        summary={
            "totalRevenue": round(total_revenue, 2),
            "totalProfit": round(total_profit, 2),
            "profitMargin": round(margin, 1),
            "growth": growth,
        },
        data=[
            {
                "date": r.day,
                "revenue": round(float(r.revenue), 2),
                "profit": round(float(r.profit), 2),
                "orders": int(r.orders),
            }
            for r in rows
        ],
    )
