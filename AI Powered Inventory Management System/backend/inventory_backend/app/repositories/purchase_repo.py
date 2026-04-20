"""Purchase repository — DB operations for purchases."""

from __future__ import annotations

from sqlalchemy.orm import Session, joinedload

from ..models.purchase import Purchase, PurchaseItem


def get_all(db: Session) -> list[Purchase]:
    return (
        db.query(Purchase)
        .options(joinedload(Purchase.items))
        .order_by(Purchase.date.desc())
        .all()
    )


def get_by_id(db: Session, purchase_id: str) -> Purchase | None:
    return (
        db.query(Purchase)
        .options(joinedload(Purchase.items))
        .filter(Purchase.id == purchase_id)
        .first()
    )


def create(db: Session, purchase: Purchase) -> Purchase:
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    # Eagerly load items
    _ = purchase.items
    return purchase


def update_status(db: Session, purchase: Purchase, new_status: str) -> Purchase:
    purchase.status = new_status
    db.commit()
    db.refresh(purchase)
    return purchase


def count(db: Session) -> int:
    return db.query(Purchase).count()


def count_by_status(db: Session, status: str) -> int:
    return db.query(Purchase).filter(Purchase.status == status).count()


def get_next_po_number(db: Session) -> str:
    """Generate next PO number like PO-2024-001."""
    from datetime import datetime, timezone
    year = datetime.now(timezone.utc).year
    count_val = db.query(Purchase).count() + 1
    return f"PO-{year}-{count_val:03d}"
