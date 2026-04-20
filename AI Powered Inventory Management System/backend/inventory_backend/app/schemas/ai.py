"""AI-related schemas matching the frontend AIInsight & ChatMessage interfaces."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel

from .base import camel_config


class AIInsightResponse(BaseModel):
    model_config = camel_config

    id: str
    type: str
    title: str
    description: str
    priority: str
    actionable: bool
    data: Any | None = None
    created_at: str


class ChatMessageSchema(BaseModel):
    """Full chat message (for frontend display)."""
    model_config = camel_config

    id: str
    role: str
    content: str
    timestamp: str


class ChatHistoryItem(BaseModel):
    """Minimal chat history item sent from frontend."""
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatHistoryItem] = []


class ChatResponse(BaseModel):
    response: str


# ── New AI feature schemas ──

class DashboardSummaryResponse(BaseModel):
    model_config = camel_config
    summary: str
    generated_at: str


class HealthScoreResponse(BaseModel):
    model_config = camel_config
    score: int
    grade: str
    breakdown: dict[str, Any]
    recommendation: str


class ReorderSuggestion(BaseModel):
    model_config = camel_config
    product_id: str
    product_name: str
    current_stock: int
    min_level: int
    daily_sales_rate: float
    suggested_quantity: int
    days_until_stockout: float
    reasoning: str


class ReorderSuggestionsResponse(BaseModel):
    model_config = camel_config
    suggestions: list[ReorderSuggestion]
    generated_at: str


class ReportNarrativeRequest(BaseModel):
    report_type: str
    summary: dict[str, Any]


class ReportNarrativeResponse(BaseModel):
    model_config = camel_config
    narrative: str
    generated_at: str


class StockoutPrediction(BaseModel):
    model_config = camel_config
    product_id: str
    product_name: str
    current_stock: int
    daily_sales_rate: float
    days_until_stockout: float
    urgency: str  # critical, warning, watch
    recommendation: str


class StockoutPredictionsResponse(BaseModel):
    model_config = camel_config
    predictions: list[StockoutPrediction]
    generated_at: str


class SalesSummaryResponse(BaseModel):
    model_config = camel_config
    summary: str
    metrics: dict[str, Any]
    generated_at: str
