"""Purchase schemas matching the frontend Purchase interface."""

from __future__ import annotations

from pydantic import BaseModel

from .base import camel_config


class PurchaseItemSchema(BaseModel):
    model_config = camel_config

    product_id: str
    product_name: str
    quantity: int
    price: float


class PurchaseResponse(BaseModel):
    model_config = camel_config

    id: str
    po_number: str
    supplier: str
    date: str
    status: str
    total_amount: float
    items: list[PurchaseItemSchema]


class PurchaseCreate(BaseModel):
    model_config = camel_config

    supplier: str
    date: str | None = None
    status: str = "pending"
    items: list[PurchaseItemSchema]


class PurchaseStatusUpdate(BaseModel):
    status: str
