"""Sale routes — /api/sales."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..auth.dependencies import require_permission
from ..schemas.sale import SaleResponse, SaleCreate, SaleStatusUpdate
from ..services import sale_service

router = APIRouter(prefix="/api/sales", tags=["Sales"])


@router.get("", response_model=list[SaleResponse])
def get_all_sales(
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("sales.view")),
):
    return sale_service.get_all(db)


@router.post("", response_model=SaleResponse, status_code=201)
def create_sale(
    data: SaleCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("sales.create")),
):
    return sale_service.create(db, data, user.id)


@router.put("/{sale_id}/status", response_model=SaleResponse)
def update_sale_status(
    sale_id: str,
    data: SaleStatusUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("sales.create")),
):
    return sale_service.update_status(db, sale_id, data.status)
