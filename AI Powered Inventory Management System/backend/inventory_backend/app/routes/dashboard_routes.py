"""Dashboard routes — /api/dashboard."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..auth.dependencies import get_current_user
from ..schemas.dashboard import (
    DashboardStatsResponse,
    SalesChartPoint,
    RevenueByCategoryPoint,
    TopProductPoint,
    MonthlyDataPoint,
    CategoryPerformancePoint,
    CustomerSegmentPoint,
)
from ..services import dashboard_service

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return dashboard_service.get_stats(db)


@router.get("/sales-chart", response_model=list[SalesChartPoint])
def get_sales_chart(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return dashboard_service.get_sales_chart(db)


@router.get("/revenue-by-category", response_model=list[RevenueByCategoryPoint])
def get_revenue_by_category(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return dashboard_service.get_revenue_by_category(db)


@router.get("/top-products", response_model=list[TopProductPoint])
def get_top_products(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return dashboard_service.get_top_products(db)


@router.get("/monthly-data", response_model=list[MonthlyDataPoint])
def get_monthly_data(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return dashboard_service.get_monthly_data(db)


@router.get("/category-performance", response_model=list[CategoryPerformancePoint])
def get_category_performance(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return dashboard_service.get_category_performance(db)


@router.get("/customer-segments", response_model=list[CustomerSegmentPoint])
def get_customer_segments(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return dashboard_service.get_customer_segments(db)
