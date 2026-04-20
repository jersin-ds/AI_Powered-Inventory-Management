"""Sale schemas matching the frontend Sale interface."""

from __future__ import annotations

from pydantic import BaseModel

from .base import camel_config


class SaleItemSchema(BaseModel):
    model_config = camel_config

    product_id: str
    product_name: str
    quantity: int
    price: float


class SaleResponse(BaseModel):
    model_config = camel_config

    id: str
    invoice_number: str
    customer: str
    date: str
    status: str
    total_amount: float
    profit: float
    items: list[SaleItemSchema]


class SaleCreate(BaseModel):
    model_config = camel_config

    customer: str
    date: str | None = None
    status: str = "pending"
    items: list[SaleItemSchema]


class SaleStatusUpdate(BaseModel):
    model_config = camel_config

    status: str
