"""Supplier schemas matching the frontend Supplier interface."""

from __future__ import annotations

from pydantic import BaseModel

from .base import camel_config


class SupplierResponse(BaseModel):
    model_config = camel_config

    id: str
    name: str
    contact_person: str
    email: str
    phone: str
    address: str
    city: str
    country: str
    products_supplied: int
    total_orders: int
    total_value: float
    rating: float
    status: str
    payment_terms: str
    created_at: str


class SupplierCreate(BaseModel):
    model_config = camel_config

    name: str
    contact_person: str
    email: str
    phone: str
    address: str = ""
    city: str = ""
    country: str = ""
    products_supplied: int = 0
    total_orders: int = 0
    total_value: float = 0.0
    rating: float = 0.0
    status: str = "active"
    payment_terms: str = "Net 30"


class SupplierUpdate(BaseModel):
    model_config = camel_config

    name: str | None = None
    contact_person: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    country: str | None = None
    products_supplied: int | None = None
    total_orders: int | None = None
    total_value: float | None = None
    rating: float | None = None
    status: str | None = None
    payment_terms: str | None = None
