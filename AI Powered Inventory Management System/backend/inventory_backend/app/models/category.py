"""Category ORM model."""

from __future__ import annotations

import uuid
import json
from datetime import datetime, timezone

from sqlalchemy import String, Text, Enum, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    product_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    subcategories: Mapped[str] = mapped_column(Text, nullable=False, default="[]")  # JSON array
    status: Mapped[str] = mapped_column(
        Enum("active", "inactive", name="category_status"),
        nullable=False,
        default="active",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationship
    products = relationship("Product", back_populates="category_rel")

    def get_subcategories(self) -> list[str]:
        try:
            return json.loads(self.subcategories)
        except (json.JSONDecodeError, TypeError):
            return []

    def set_subcategories(self, value: list[str]) -> None:
        self.subcategories = json.dumps(value)

    def __repr__(self) -> str:
        return f"<Category {self.name}>"
