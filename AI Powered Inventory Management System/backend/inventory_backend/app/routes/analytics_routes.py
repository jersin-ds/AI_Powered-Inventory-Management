"""Analytics routes — /api/analytics."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..auth.dependencies import require_permission
from ..schemas.dashboard import (
    MonthlyDataPoint,
    CategoryPerformancePoint,
    CustomerSegmentPoint,
)
from ..services import analytics_service

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/monthly", response_model=list[MonthlyDataPoint])
def get_monthly_data(
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("reports.view")),
):
    return analytics_service.get_monthly_data(db)


@router.get("/category-performance", response_model=list[CategoryPerformancePoint])
def get_category_performance(
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("reports.view")),
):
    return analytics_service.get_category_performance(db)


@router.get("/customer-segments", response_model=list[CustomerSegmentPoint])
def get_customer_segments(
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("reports.view")),
):
    return analytics_service.get_customer_segments(db)
