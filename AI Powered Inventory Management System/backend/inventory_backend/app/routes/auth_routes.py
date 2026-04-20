"""Authentication routes — POST /api/auth/login, POST /api/auth/logout."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..auth.security import verify_password
from ..auth.jwt import create_access_token
from ..auth.dependencies import get_current_user
from ..schemas.base import camel_config

router = APIRouter(prefix="/api/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginUserResponse(BaseModel):
    model_config = camel_config

    id: str
    email: str
    name: str
    role: str
    avatar: str | None = None


class LoginResponse(BaseModel):
    user: LoginUserResponse
    token: str


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if user.status == "inactive":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )

    token = create_access_token(user.id, user.role)

    # Update last login
    user.last_login = datetime.now(timezone.utc)
    db.commit()

    return LoginResponse(
        user=LoginUserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role,
            avatar=user.avatar,
        ),
        token=token,
    )


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    return {"success": True}
