"""Warehouse repository — DB operations for warehouses."""

from __future__ import annotations

from sqlalchemy.orm import Session

from ..models.warehouse import Warehouse, WarehouseStock


def get_all(db: Session) -> list[Warehouse]:
    return db.query(Warehouse).order_by(Warehouse.name).all()


def get_by_id(db: Session, warehouse_id: str) -> Warehouse | None:
    return db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()


def create(db: Session, warehouse: Warehouse) -> Warehouse:
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    return warehouse


def update(db: Session, warehouse: Warehouse, updates: dict) -> Warehouse:
    for key, value in updates.items():
        if value is not None and hasattr(warehouse, key):
            setattr(warehouse, key, value)
    db.commit()
    db.refresh(warehouse)
    return warehouse


def delete(db: Session, warehouse: Warehouse) -> None:
    db.delete(warehouse)
    db.commit()


# ── WarehouseStock ──

def get_stock(db: Session, warehouse_id: str, product_id: str) -> WarehouseStock | None:
    return (
        db.query(WarehouseStock)
        .filter(WarehouseStock.warehouse_id == warehouse_id, WarehouseStock.product_id == product_id)
        .first()
    )


def upsert_stock(db: Session, warehouse_id: str, product_id: str, quantity: int) -> WarehouseStock:
    stock = get_stock(db, warehouse_id, product_id)
    if stock:
        stock.quantity = quantity
    else:
        stock = WarehouseStock(warehouse_id=warehouse_id, product_id=product_id, quantity=quantity)
        db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock
