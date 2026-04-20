"""User routes — /api/users + /me profile."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..auth.dependencies import get_current_user, require_role
from ..schemas.user import (
    UserResponse,
    UserCreate,
    UserUpdate,
    ProfileUpdate,
    PasswordUpdate,
    NotificationSettings,
)
from ..services import user_service

router = APIRouter(prefix="/api/users", tags=["Users"])


# ── /me endpoints (any authenticated user) ──

@router.get("/me/profile", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return user_service.get_by_id(db, current_user.id)


@router.put("/me/profile", response_model=UserResponse)
def update_my_profile(
    data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return user_service.update_profile(db, current_user.id, data.name, data.email)


@router.put("/me/password")
def update_my_password(
    data: PasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_service.update_password(db, current_user.id, data.current_password, data.new_password)
    return {"success": True}


@router.get("/me/notifications")
def get_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return user_service.get_notifications(db, current_user.id)


@router.put("/me/notifications")
def update_notifications(
    data: NotificationSettings,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    settings = data.model_dump()
    return user_service.update_notifications(db, current_user.id, {
        "lowStockAlerts": settings.get("low_stock_alerts", True),
        "aiInsights": settings.get("ai_insights", True),
        "purchaseOrders": settings.get("purchase_orders", True),
    })


# ── Admin CRUD ──

@router.get("", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    _user: User = Depends(require_role("admin")),
):
    return user_service.get_all(db)


@router.post("", response_model=UserResponse, status_code=201)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(require_role("admin")),
):
    return user_service.create(db, data)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    data: UserUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(require_role("admin")),
):
    return user_service.update(db, user_id, data)


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    _user: User = Depends(require_role("admin")),
):
    user_service.delete(db, user_id)
