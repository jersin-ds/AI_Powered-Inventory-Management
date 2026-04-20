"""Stock routes — /api/stock/low, /api/stock/out, /api/stock/auto-reorder, /api/stock/adjust."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..auth.dependencies import require_permission
from ..schemas.product import ProductResponse
from ..services import product_service, stock_service

router = APIRouter(prefix="/api/stock", tags=["Stock"])


@router.get("/low", response_model=list[ProductResponse])
def get_low_stock(
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("stock.view")),
):
    return product_service.get_low_stock(db)


@router.get("/out", response_model=list[ProductResponse])
def get_out_of_stock(
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("stock.view")),
):
    return product_service.get_out_of_stock(db)


@router.post("/auto-reorder")
def auto_reorder(
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("stock.manage")),
):
    """Scan low/out-of-stock items, group by supplier, create purchase orders."""
    return stock_service.auto_reorder(db, user.id)


class StockAdjustment(BaseModel):
    product_id: str
    quantity: int
    reason: str = ""


@router.post("/adjust")
def adjust_stock(
    adj: StockAdjustment,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("stock.manage")),
):
    """Manually adjust stock quantity (positive = add, negative = remove)."""
    return stock_service.adjust_stock(db, adj.product_id, adj.quantity, adj.reason, user.id)
