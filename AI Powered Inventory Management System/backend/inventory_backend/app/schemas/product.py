"""Product schemas matching the frontend Product interface."""

from __future__ import annotations

from pydantic import BaseModel

from .base import camel_config


class ProductResponse(BaseModel):
    model_config = camel_config

    id: str
    sku: str
    name: str
    category: str  # category name, not id
    subcategory: str
    supplier: str  # supplier name, not id
    cost_price: float
    sell_price: float
    stock_qty: int
    min_level: int
    barcode: str
    image: str | None = None
    status: str
    created_at: str


class ProductCreate(BaseModel):
    model_config = camel_config

    sku: str | None = None  # auto-generated if not provided
    name: str
    category: str
    subcategory: str = ""
    supplier: str
    cost_price: float
    sell_price: float
    stock_qty: int = 0
    min_level: int = 10
    barcode: str = ""
    image: str | None = None
    status: str | None = None  # auto-computed


class ProductUpdate(BaseModel):
    model_config = camel_config

    name: str | None = None
    category: str | None = None
    subcategory: str | None = None
    supplier: str | None = None
    cost_price: float | None = None
    sell_price: float | None = None
    stock_qty: int | None = None
    min_level: int | None = None
    barcode: str | None = None
    image: str | None = None
    status: str | None = None
