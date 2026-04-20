"""User ORM model."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Enum, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(
        Enum("admin", "inventory_manager", "sales_staff", name="user_role"),
        nullable=False,
        default="sales_staff",
    )
    avatar: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("active", "inactive", name="user_status"),
        nullable=False,
        default="active",
    )
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Notification preferences (JSON-like booleans)
    notify_low_stock: Mapped[bool] = mapped_column(default=True)
    notify_ai_insights: Mapped[bool] = mapped_column(default=True)
    notify_purchase_orders: Mapped[bool] = mapped_column(default=True)

    def __repr__(self) -> str:
        return f"<User {self.email} ({self.role})>"
