"""Dashboard & analytics & report schemas."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from .base import camel_config


# ── Dashboard ──────────────────────────────────────────────

class DashboardStatsResponse(BaseModel):
    model_config = camel_config

    total_revenue: float
    total_profit: float
    total_products: int
    total_orders: int
    low_stock_items: int
    out_of_stock_items: int
    pending_orders: int
    revenue_growth: float
    profit_growth: float


class SalesChartPoint(BaseModel):
    date: str
    sales: float
    profit: float


class RevenueByCategoryPoint(BaseModel):
    category: str
    value: float
    percentage: float


class TopProductPoint(BaseModel):
    id: str
    name: str
    sales: int
    revenue: float


# ── Analytics ──────────────────────────────────────────────

class MonthlyDataPoint(BaseModel):
    month: str
    revenue: float
    expenses: float
    profit: float
    orders: int


class CategoryPerformancePoint(BaseModel):
    category: str
    sales: float
    growth: float
    margin: float


class CustomerSegmentPoint(BaseModel):
    segment: str
    value: float


# ── Reports ────────────────────────────────────────────────

class ReportSummary(BaseModel):
    model_config = camel_config

    title: str
    period: str
    summary: dict[str, Any]
    data: list[Any]
