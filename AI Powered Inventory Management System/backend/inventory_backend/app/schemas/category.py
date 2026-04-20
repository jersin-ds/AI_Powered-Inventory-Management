"""Category schemas matching the frontend Category interface."""

from __future__ import annotations

from pydantic import BaseModel

from .base import camel_config


class CategoryResponse(BaseModel):
    model_config = camel_config

    id: str
    name: str
    description: str
    product_count: int
    subcategories: list[str]
    status: str
    created_at: str


class CategoryCreate(BaseModel):
    name: str
    description: str = ""
    subcategories: list[str] = []
    status: str = "active"


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    subcategories: list[str] | None = None
    status: str | None = None
