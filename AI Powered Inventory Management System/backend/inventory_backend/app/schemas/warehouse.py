"""Warehouse schemas matching the frontend Warehouse interface."""

from __future__ import annotations

from pydantic import BaseModel

from .base import camel_config


class WarehouseResponse(BaseModel):
    model_config = camel_config

    id: str
    name: str
    location: str
    capacity: int
    current_stock: int
    manager: str
    status: str


class WarehouseCreate(BaseModel):
    name: str
    location: str
    capacity: int = 0
    current_stock: int = 0
    manager: str = ""
    status: str = "active"


class WarehouseUpdate(BaseModel):
    name: str | None = None
    location: str | None = None
    capacity: int | None = None
    current_stock: int | None = None
    manager: str | None = None
    status: str | None = None
