"""Sale repository — DB operations for sales."""

from __future__ import annotations

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from ..models.sale import Sale, SaleItem


def get_all(db: Session) -> list[Sale]:
    return (
        db.query(Sale)
        .options(joinedload(Sale.items))
        .order_by(Sale.date.desc())
        .all()
    )


def get_by_id(db: Session, sale_id: str) -> Sale | None:
    return (
        db.query(Sale)
        .options(joinedload(Sale.items))
        .filter(Sale.id == sale_id)
        .first()
    )


def create(db: Session, sale: Sale) -> Sale:
    db.add(sale)
    db.commit()
    db.refresh(sale)
    _ = sale.items
    return sale


def count(db: Session) -> int:
    return db.query(Sale).count()


def total_revenue(db: Session) -> float:
    result = db.query(func.sum(Sale.total_amount)).filter(Sale.status == "completed").scalar()
    return float(result or 0.0)


def total_profit(db: Session) -> float:
    result = db.query(func.sum(Sale.profit)).filter(Sale.status == "completed").scalar()
    return float(result or 0.0)


def get_next_invoice_number(db: Session) -> str:
    """Generate next invoice number like INV-2024-001."""
    from datetime import datetime, timezone
    year = datetime.now(timezone.utc).year
    count_val = db.query(Sale).count() + 1
    return f"INV-{year}-{count_val:03d}"
