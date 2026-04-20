"""Cerebras LLM client wrapper."""

from __future__ import annotations

import logging
import re
from cerebras.cloud.sdk import Cerebras

from ..config import settings

logger = logging.getLogger(__name__)

_client: Cerebras | None = None


def _get_client() -> Cerebras:
    global _client
    if _client is None:
        _client = Cerebras(api_key=settings.cerebras_api_key)
    return _client


def complete(system_prompt: str, user_prompt: str) -> str:
    """Send a chat completion request to Cerebras and return the text response."""
    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=settings.cerebras_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=512,
            temperature=0.7,
        )
        return _strip_markdown(response.choices[0].message.content or "")
    except Exception as e:
        logger.error(f"Cerebras API error: {e}")
        # Fallback response if API fails
        return _fallback_response(user_prompt)


def complete_with_history(system_prompt: str, messages: list[dict]) -> str:
    """Send a multi-turn chat to Cerebras."""
    try:
        client = _get_client()
        all_messages = [{"role": "system", "content": system_prompt}] + messages
        response = client.chat.completions.create(
            model=settings.cerebras_model,
            messages=all_messages,
            max_tokens=512,
            temperature=0.7,
        )
        return _strip_markdown(response.choices[0].message.content or "")
    except Exception as e:
        logger.error(f"Cerebras API error: {e}")
        return _fallback_response(messages[-1]["content"] if messages else "")


def _strip_markdown(text: str) -> str:
    """Remove markdown formatting from AI responses."""
    text = re.sub(r'#{1,6}\s*', '', text)          # ## headers
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # **bold**
    text = re.sub(r'\*(.*?)\*', r'\1', text)        # *italic*
    return text.strip()


def _fallback_response(user_message: str) -> str:
    """Provide intelligent fallback responses when Cerebras API is unavailable."""
    lower = user_message.lower()

    if "stock" in lower or "inventory" in lower:
        return (
            "Based on current inventory levels, I can see items that need attention. "
            "Check the Stock page for low-stock and out-of-stock items. "
            "I recommend reviewing reorder points and placing purchase orders for critical items."
        )
    if "sales" in lower or "revenue" in lower:
        return (
            "Your sales data is available on the Dashboard and Reports pages. "
            "Check the Analytics section for detailed revenue breakdowns by category and trends over time."
        )
    if "demand" in lower or "forecast" in lower:
        return (
            "Demand forecasting analyzes your historical sales data to predict future needs. "
            "Check the AI Insights page for specific product forecasts and recommended order quantities."
        )
    if "price" in lower or "pricing" in lower:
        return (
            "Price optimization considers your cost prices, current sell prices, and sales velocity. "
            "Review the AI Insights page for specific pricing recommendations."
        )
    if "help" in lower or "what can you" in lower:
        return (
            "I can help you with:\n\n"
            "Inventory Analysis - Stock levels, reorder recommendations\n"
            "Sales Insights - Revenue trends, top products\n"
            "Demand Forecasting - Predict future demand\n"
            "Price Optimization - Pricing strategy suggestions\n"
            "Alerts - Low stock, expiry risks, anomalies\n\n"
            "Just ask me anything about your inventory!"
        )

    return (
        "I can only help with inventory-related questions such as stock levels, "
        "sales data, product details, reorder suggestions, and business analytics. "
        "Please ask me something about your inventory!"
    )
