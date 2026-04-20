"""Supplier repository — DB operations for suppliers."""

from __future__ import annotations

from sqlalchemy.orm import Session

from ..models.supplier import Supplier


def get_all(db: Session) -> list[Supplier]:
    return db.query(Supplier).order_by(Supplier.name).all()


def get_by_id(db: Session, supplier_id: str) -> Supplier | None:
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()


def get_by_name(db: Session, name: str) -> Supplier | None:
    return db.query(Supplier).filter(Supplier.name == name).first()


def create(db: Session, supplier: Supplier) -> Supplier:
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


def update(db: Session, supplier: Supplier, updates: dict) -> Supplier:
    for key, value in updates.items():
        if value is not None and hasattr(supplier, key):
            setattr(supplier, key, value)
    db.commit()
    db.refresh(supplier)
    return supplier


def delete(db: Session, supplier: Supplier) -> None:
    db.delete(supplier)
    db.commit()


def count(db: Session) -> int:
    return db.query(Supplier).count()
