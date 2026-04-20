"""Auth request / response schemas."""

from __future__ import annotations

from pydantic import BaseModel, EmailStr

from .base import camel_config


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthUserResponse(BaseModel):
    model_config = camel_config

    id: str
    email: str
    name: str
    role: str
    avatar: str | None = None


class LoginResponse(BaseModel):
    model_config = camel_config

    user: AuthUserResponse
    token: str
