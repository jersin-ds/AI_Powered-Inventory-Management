"""Purchase routes — /api/purchases."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..auth.dependencies import require_permission
from ..schemas.purchase import PurchaseResponse, PurchaseCreate, PurchaseStatusUpdate
from ..services import purchase_service

router = APIRouter(prefix="/api/purchases", tags=["Purchases"])


@router.get("", response_model=list[PurchaseResponse])
def get_all_purchases(
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("purchases.view")),
):
    return purchase_service.get_all(db)


@router.post("", response_model=PurchaseResponse, status_code=201)
def create_purchase(
    data: PurchaseCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("purchases.create")),
):
    return purchase_service.create(db, data, user.id)


@router.put("/{purchase_id}/status", response_model=PurchaseResponse)
def update_purchase_status(
    purchase_id: str,
    data: PurchaseStatusUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("purchases.create")),
):
    return purchase_service.update_status(db, purchase_id, data.status)
