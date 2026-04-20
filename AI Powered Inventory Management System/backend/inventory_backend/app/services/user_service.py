"""User service — business logic for user CRUD and profile management."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.user import User
from ..repositories import user_repo
from ..auth.security import hash_password, verify_password
from ..schemas.user import UserCreate, UserUpdate, UserResponse


def _to_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        avatar=user.avatar,
        status=user.status,
        last_login=user.last_login.isoformat() if user.last_login else None,
        created_at=str(user.created_at)[:10] if user.created_at else "",
    )


def get_all(db: Session) -> list[UserResponse]:
    users = user_repo.get_all(db)
    return [_to_response(u) for u in users]


def get_by_id(db: Session, user_id: str) -> UserResponse:
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _to_response(user)


def create(db: Session, data: UserCreate) -> UserResponse:
    existing = user_repo.get_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role,
        status=data.status,
    )
    user = user_repo.create(db, user)
    return _to_response(user)


def update(db: Session, user_id: str, data: UserUpdate) -> UserResponse:
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updates = data.model_dump(exclude_unset=True)
    user = user_repo.update(db, user, updates)
    return _to_response(user)


def delete(db: Session, user_id: str) -> None:
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_repo.delete(db, user)


def update_profile(db: Session, user_id: str, name: str | None, email: str | None) -> UserResponse:
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updates: dict = {}
    if name:
        updates["name"] = name
    if email:
        # Check uniqueness
        existing = user_repo.get_by_email(db, email)
        if existing and existing.id != user_id:
            raise HTTPException(status_code=400, detail="Email already in use")
        updates["email"] = email

    user = user_repo.update(db, user, updates)
    return _to_response(user)


def update_password(db: Session, user_id: str, current_password: str, new_password: str) -> None:
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    user.password_hash = hash_password(new_password)
    db.commit()


def get_notifications(db: Session, user_id: str) -> dict:
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "lowStockAlerts": user.notify_low_stock,
        "aiInsights": user.notify_ai_insights,
        "purchaseOrders": user.notify_purchase_orders,
    }


def update_notifications(db: Session, user_id: str, settings: dict) -> dict:
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if "lowStockAlerts" in settings:
        user.notify_low_stock = settings["lowStockAlerts"]
    if "aiInsights" in settings:
        user.notify_ai_insights = settings["aiInsights"]
    if "purchaseOrders" in settings:
        user.notify_purchase_orders = settings["purchaseOrders"]

    db.commit()
    db.refresh(user)

    return {
        "lowStockAlerts": user.notify_low_stock,
        "aiInsights": user.notify_ai_insights,
        "purchaseOrders": user.notify_purchase_orders,
    }
