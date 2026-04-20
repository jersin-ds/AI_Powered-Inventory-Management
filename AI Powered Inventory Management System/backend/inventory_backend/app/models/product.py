"""Product ORM model."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    category_id: Mapped[str] = mapped_column(String(36), ForeignKey("categories.id"), nullable=False)
    subcategory: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    supplier_id: Mapped[str] = mapped_column(String(36), ForeignKey("suppliers.id"), nullable=False)
    cost_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    sell_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    stock_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    min_level: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    barcode: Mapped[str] = mapped_column(String(50), nullable=False, default="")
    image: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    category_rel = relationship("Category", back_populates="products")
    supplier_rel = relationship("Supplier", back_populates="products")
    warehouse_stocks = relationship("WarehouseStock", back_populates="product", cascade="all, delete-orphan")
    batches = relationship("Batch", back_populates="product", cascade="all, delete-orphan")

    @property
    def computed_status(self) -> str:
        if self.stock_qty <= 0:
            return "out_of_stock"
        if self.stock_qty < self.min_level:
            return "low_stock"
        return "active"

    def sync_status(self) -> None:
        """Update status based on current stock levels."""
        self.status = self.computed_status

    def __repr__(self) -> str:
        return f"<Product {self.sku} - {self.name}>"
