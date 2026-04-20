"""Report routes — /api/reports."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..auth.dependencies import require_permission
from ..schemas.dashboard import ReportSummary
from ..services import report_service

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/sales", response_model=ReportSummary)
def sales_report(
    range: str = Query("30days", alias="range"),
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("reports.view")),
):
    return report_service.sales_report(db, range)


@router.get("/purchases", response_model=ReportSummary)
def purchases_report(
    range: str = Query("30days", alias="range"),
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("reports.view")),
):
    return report_service.purchases_report(db, range)


@router.get("/inventory", response_model=ReportSummary)
def inventory_report(
    range: str = Query("30days", alias="range"),
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("reports.view")),
):
    return report_service.inventory_report(db, range)


@router.get("/profit", response_model=ReportSummary)
def profit_report(
    range: str = Query("30days", alias="range"),
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("reports.view")),
):
    return report_service.profit_report(db, range)
