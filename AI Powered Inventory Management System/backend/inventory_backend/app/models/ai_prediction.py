"""AI Prediction ORM model."""

from __future__ import annotations

import uuid
import json
from datetime import datetime, timezone

from sqlalchemy import String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class AIPrediction(Base):
    __tablename__ = "ai_predictions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")
    actionable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    data: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    def get_data(self) -> dict | None:
        if self.data is None:
            return None
        try:
            return json.loads(self.data)
        except (json.JSONDecodeError, TypeError):
            return None

    def set_data(self, value: dict | None) -> None:
        self.data = json.dumps(value) if value is not None else None

    def __repr__(self) -> str:
        return f"<AIPrediction {self.type}: {self.title}>"
