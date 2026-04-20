"""User schemas matching the frontend User interface."""

from __future__ import annotations

from pydantic import BaseModel, EmailStr

from .base import camel_config


class UserResponse(BaseModel):
    model_config = camel_config

    id: str
    name: str
    email: str
    role: str
    avatar: str | None = None
    status: str
    last_login: str | None = None
    created_at: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = "password123"
    role: str = "sales_staff"
    status: str = "active"


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    role: str | None = None
    status: str | None = None


class ProfileUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class PasswordUpdate(BaseModel):
    model_config = camel_config

    current_password: str
    new_password: str


class NotificationSettings(BaseModel):
    model_config = camel_config

    low_stock_alerts: bool = True
    ai_insights: bool = True
    purchase_orders: bool = True
