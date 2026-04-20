"""AI routes — /api/ai (insights, chat, prompts, generate, dashboard-summary, health-score, etc.)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..auth.dependencies import require_permission
from ..schemas.ai import (
    AIInsightResponse,
    ChatRequest,
    ChatResponse,
    DashboardSummaryResponse,
    HealthScoreResponse,
    ReorderSuggestionsResponse,
    ReportNarrativeRequest,
    ReportNarrativeResponse,
    StockoutPredictionsResponse,
    SalesSummaryResponse,
)
from ..ai import ai_service

router = APIRouter(prefix="/api/ai", tags=["AI"])


@router.get("/insights", response_model=list[AIInsightResponse])
def get_insights(
    type: str | None = Query(None, description="Filter by insight type"),
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("ai.view")),
):
    return ai_service.get_insights(db, type)


@router.post("/chat", response_model=ChatResponse)
def chat(
    data: ChatRequest,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("ai.view")),
):
    response = ai_service.chat(db, data.message, data.history)
    return ChatResponse(response=response)


@router.get("/prompts", response_model=list[str])
def get_prompts(
    _user: User = Depends(require_permission("ai.view")),
):
    return ai_service.get_suggested_prompts()


@router.post("/generate-insights", response_model=list[AIInsightResponse])
def generate_insights(
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("ai.view")),
):
    """Trigger fresh AI analysis of all inventory data."""
    return ai_service.generate_insights(db)


@router.get("/dashboard-summary", response_model=DashboardSummaryResponse)
def dashboard_summary(
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("ai.view")),
):
    """Generate an AI-powered natural language dashboard summary."""
    return ai_service.get_dashboard_summary(db)


@router.get("/health-score", response_model=HealthScoreResponse)
def health_score(
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("ai.view")),
):
    """Calculate inventory health score (0-100) with AI recommendation."""
    return ai_service.get_health_score(db)


@router.get("/reorder-suggestions", response_model=ReorderSuggestionsResponse)
def reorder_suggestions(
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("ai.view")),
):
    """Get AI-powered smart reorder suggestions for low-stock products."""
    return ai_service.get_reorder_suggestions(db)


@router.post("/report-narrative", response_model=ReportNarrativeResponse)
def report_narrative(
    data: ReportNarrativeRequest,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("ai.view")),
):
    """Generate an AI narrative summary for a report."""
    return ai_service.generate_report_narrative(db, data.report_type, data.summary)


@router.get("/stockout-predictions", response_model=StockoutPredictionsResponse)
def stockout_predictions(
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("ai.view")),
):
    """Predict which products will run out of stock and when."""
    return ai_service.get_stockout_predictions(db)


@router.get("/sales-summary", response_model=SalesSummaryResponse)
def sales_summary(
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("ai.view")),
):
    """Get AI-generated sales trend analysis."""
    return ai_service.get_sales_summary(db)
