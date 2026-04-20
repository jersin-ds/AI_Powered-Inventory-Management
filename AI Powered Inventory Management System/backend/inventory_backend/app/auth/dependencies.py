"""FastAPI dependencies for authentication and role-based access control.

Mirrors the frontend's `hasPermission()` logic from auth-store.ts including
the 'all' wildcard for admin role.
"""

from __future__ import annotations

from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from .jwt import verify_token

bearer_scheme = HTTPBearer()

# ── Role → Permissions map (mirrors frontend auth-store.ts) ──

ROLE_PERMISSIONS: dict[str, list[str]] = {
    "admin": ["all"],
    "inventory_manager": [
        "products.view",
        "products.create",
        "products.edit",
        "products.delete",
        "stock.view",
        "stock.manage",
        "warehouses.view",
        "warehouses.manage",
        "purchases.view",
        "purchases.create",
        "reports.view",
        "ai.view",
        "ai.suggestions",
    ],
    "sales_staff": [
        "products.view",
        "sales.view",
        "sales.create",
        "reports.view-limited",
        "ai.view",
    ],
}


def _has_permission(role: str, permission: str) -> bool:
    perms = ROLE_PERMISSIONS.get(role, [])
    return "all" in perms or permission in perms


# ── Dependencies ──

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Extract and validate the JWT, return the current User from the DB."""
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


def require_permission(permission: str) -> Callable:
    """Return a dependency that asserts the current user has a specific permission."""

    async def _checker(current_user: User = Depends(get_current_user)) -> User:
        if not _has_permission(current_user.role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required",
            )
        return current_user

    return _checker


def require_role(*roles: str) -> Callable:
    """Return a dependency that asserts the current user has one of the given roles."""

    async def _checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"One of roles {roles} required",
            )
        return current_user

    return _checker
