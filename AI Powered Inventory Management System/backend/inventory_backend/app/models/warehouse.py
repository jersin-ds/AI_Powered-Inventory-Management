"""Warehouse & WarehouseStock ORM models."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(String(200), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    current_stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    manager: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    status: Mapped[str] = mapped_column(
        Enum("active", "inactive", name="warehouse_status"),
        nullable=False,
        default="active",
    )

    # Relationships
    stocks = relationship("WarehouseStock", back_populates="warehouse", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Warehouse {self.name}>"


class WarehouseStock(Base):
    __tablename__ = "warehouse_stock"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    warehouse_id: Mapped[str] = mapped_column(String(36), ForeignKey("warehouses.id"), nullable=False)
    product_id: Mapped[str] = mapped_column(String(36), ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Relationships
    warehouse = relationship("Warehouse", back_populates="stocks")
    product = relationship("Product", back_populates="warehouse_stocks")

    def __repr__(self) -> str:
        return f"<WarehouseStock wh={self.warehouse_id} prod={self.product_id} qty={self.quantity}>"
