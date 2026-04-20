"""Product repository — DB operations for products."""

from __future__ import annotations

from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..models.product import Product


def get_all(db: Session) -> list[Product]:
    return db.query(Product).order_by(Product.created_at.desc()).all()


def get_by_id(db: Session, product_id: str) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()


def get_by_sku(db: Session, sku: str) -> Product | None:
    return db.query(Product).filter(Product.sku == sku).first()


def create(db: Session, product: Product) -> Product:
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update(db: Session, product: Product, updates: dict) -> Product:
    for key, value in updates.items():
        if value is not None and hasattr(product, key):
            setattr(product, key, value)
    product.sync_status()
    db.commit()
    db.refresh(product)
    return product


def delete(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()


def search(db: Session, query: str) -> list[Product]:
    pattern = f"%{query}%"
    return (
        db.query(Product)
        .filter(
            or_(
                Product.name.ilike(pattern),
                Product.sku.ilike(pattern),
            )
        )
        .all()
    )


def get_low_stock(db: Session) -> list[Product]:
    return db.query(Product).filter(Product.status == "low_stock").all()


def get_out_of_stock(db: Session) -> list[Product]:
    return db.query(Product).filter(Product.status == "out_of_stock").all()


def count(db: Session) -> int:
    return db.query(Product).count()


def count_by_status(db: Session, status: str) -> int:
    return db.query(Product).filter(Product.status == status).count()


def get_next_sku_number(db: Session) -> int:
    """Return next sequential SKU number."""
    last = db.query(Product).order_by(Product.sku.desc()).first()
    if last and last.sku.startswith("SKU"):
        try:
            return int(last.sku[3:]) + 1
        except ValueError:
            pass
    return 1


def get_by_category_id(db: Session, category_id: str) -> list[Product]:
    return db.query(Product).filter(Product.category_id == category_id).all()


def count_by_category(db: Session, category_id: str) -> int:
    return db.query(Product).filter(Product.category_id == category_id).count()
