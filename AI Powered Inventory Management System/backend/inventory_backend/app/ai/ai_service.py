"""AI service — orchestrates all AI features (insights, chat, forecasting)."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.ai_prediction import AIPrediction
from ..models.product import Product
from ..models.sale import Sale, SaleItem
from ..models.batch import Batch
from ..models.category import Category
from ..repositories import ai_prediction_repo, product_repo
from ..schemas.ai import (
    AIInsightResponse,
    ChatHistoryItem,
    DashboardSummaryResponse,
    HealthScoreResponse,
    ReorderSuggestion,
    ReorderSuggestionsResponse,
    ReportNarrativeResponse,
    StockoutPrediction,
    StockoutPredictionsResponse,
    SalesSummaryResponse,
)
from . import cerebras_client
from .prompts import (
    chat_system_prompt,
    demand_forecast_prompt,
    dead_stock_prompt,
    anomaly_detection_prompt,
    price_optimization_prompt,
    expiry_risk_prompt,
    dashboard_summary_prompt,
    health_score_prompt,
    reorder_suggestion_prompt,
    report_narrative_prompt,
    stockout_prediction_prompt,
    sales_summary_prompt,
)

logger = logging.getLogger(__name__)


# ── Helpers ──

def _build_inventory_context(db: Session) -> str:
    """Build a text summary of inventory state for the AI chat context."""
    products = db.query(Product).all()
    lines = ["=== Current Inventory ==="]
    for p in products:
        cat_name = p.category_rel.name if p.category_rel else "Unknown"
        lines.append(
            f"- {p.name} (SKU: {p.sku}): stock={p.stock_qty}, "
            f"min={p.min_level}, cost=₹{p.cost_price}, sell=₹{p.sell_price}, "
            f"status={p.status}, category={cat_name}"
        )

    # Sales summary
    from sqlalchemy import func
    total_rev = db.query(func.sum(Sale.total_amount)).filter(Sale.status == "completed").scalar() or 0
    total_prof = db.query(func.sum(Sale.profit)).filter(Sale.status == "completed").scalar() or 0
    sale_count = db.query(Sale).filter(Sale.status == "completed").count()

    lines.append(f"\n=== Sales Summary ===")
    lines.append(f"Completed sales: {sale_count}, Revenue: ₹{total_rev:,.2f}, Profit: ₹{total_prof:,.2f}")

    low_stock = [p for p in products if p.status == "low_stock"]
    out_of_stock = [p for p in products if p.status == "out_of_stock"]
    lines.append(f"\n=== Alerts ===")
    lines.append(f"Low stock items: {len(low_stock)}")
    lines.append(f"Out of stock items: {len(out_of_stock)}")
    for p in low_stock:
        lines.append(f"  ⚠️ {p.name}: {p.stock_qty} units (min: {p.min_level})")
    for p in out_of_stock:
        lines.append(f"  🔴 {p.name}: OUT OF STOCK")

    return "\n".join(lines)


def _prediction_to_response(pred: AIPrediction) -> AIInsightResponse:
    return AIInsightResponse(
        id=pred.id,
        type=pred.type,
        title=pred.title,
        description=pred.description,
        priority=pred.priority,
        actionable=pred.actionable,
        data=pred.get_data(),
        created_at=str(pred.created_at)[:10] if pred.created_at else "",
    )


# ── Public API ──

def get_insights(db: Session, insight_type: str | None = None) -> list[AIInsightResponse]:
    """Get stored AI insights/predictions."""
    if insight_type:
        predictions = ai_prediction_repo.get_by_type(db, insight_type)
    else:
        predictions = ai_prediction_repo.get_all(db)
    return [_prediction_to_response(p) for p in predictions]


def chat(db: Session, message: str, history: list[ChatHistoryItem]) -> str:
    """AI chat with inventory context."""
    context = _build_inventory_context(db)
    system = chat_system_prompt(context)

    # Build message history for Cerebras
    messages = []
    for msg in history:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": message})

    return cerebras_client.complete_with_history(system, messages)


def get_suggested_prompts() -> list[str]:
    """Return suggested chat prompts matching the frontend."""
    return [
        "What's my current stock status?",
        "Show me sales performance this month",
        "What items should I reorder?",
        "Analyze demand forecast",
        "Any pricing recommendations?",
        "Which products are slow-moving?",
    ]


def generate_insights(db: Session) -> list[AIInsightResponse]:
    """Generate fresh AI insights by analyzing current data with Cerebras."""
    products = db.query(Product).all()
    products_by_id = {str(p.id): p for p in products}
    products_by_sku = {str(p.sku): p for p in products}
    products_by_name = {str(p.name).lower(): p for p in products}
    product_data = json.dumps([
        {
            "id": p.id,
            "name": p.name,
            "sku": p.sku,
            "stockQty": p.stock_qty,
            "minLevel": p.min_level,
            "costPrice": p.cost_price,
            "sellPrice": p.sell_price,
            "status": p.status,
        }
        for p in products
    ], indent=2)

    # Sales data
    sales = db.query(Sale).all()
    sales_data = json.dumps([
        {
            "id": s.id,
            "customer": s.customer,
            "totalAmount": s.total_amount,
            "profit": s.profit,
            "status": s.status,
            "itemCount": len(s.items) if s.items else 0,
        }
        for s in sales
    ], indent=2)

    # Batch data for expiry
    batches = db.query(Batch).all()
    batch_data = json.dumps([
        {
            "productId": b.product_id,
            "batchNumber": b.batch_number,
            "quantity": b.quantity,
            "expiryDate": str(b.expiry_date) if b.expiry_date else None,
        }
        for b in batches
    ], indent=2)

    new_predictions: list[AIPrediction] = []

    # Generate each type of insight
    insight_generators = [
        ("demand_forecast", demand_forecast_prompt(product_data), "high"),
        ("dead_stock", dead_stock_prompt(product_data), "medium"),
        ("anomaly", anomaly_detection_prompt(sales_data), "high"),
        ("price_optimization", price_optimization_prompt(product_data), "low"),
        ("expiry_risk", expiry_risk_prompt(batch_data), "medium"),
    ]

    for insight_type, prompt, default_priority in insight_generators:
        try:
            raw_response = cerebras_client.complete(
                "You are an inventory analytics AI. Respond only with valid JSON.",
                prompt,
            )

            # Try to parse AI response as JSON
            data = _parse_ai_json(raw_response)

            if isinstance(data, list):
                for item in data:
                    if not isinstance(item, dict):
                        continue
                    item = _enrich_item_with_product(item, products_by_id, products_by_sku, products_by_name)
                    pred = AIPrediction(
                        type=insight_type,
                        title=_generate_title(insight_type, item),
                        description=_build_insight_description(item, insight_type),
                        priority=item.get("priority", default_priority),
                        actionable=True,
                    )
                    pred.set_data(item)
                    new_predictions.append(pred)
            elif isinstance(data, dict):
                data = _enrich_item_with_product(data, products_by_id, products_by_sku, products_by_name)
                pred = AIPrediction(
                    type=insight_type,
                    title=_generate_title(insight_type, data),
                    description=_build_insight_description(data, insight_type),
                    priority=data.get("priority", default_priority),
                    actionable=True,
                )
                pred.set_data(data)
                new_predictions.append(pred)

        except Exception as e:
            logger.error(f"Failed to generate {insight_type} insight: {e}")

    # Save new predictions (clear old ones first)
    if new_predictions:
        ai_prediction_repo.delete_all(db)
        for pred in new_predictions:
            ai_prediction_repo.create(db, pred)

    return [_prediction_to_response(p) for p in new_predictions]


def _parse_ai_json(text: str) -> dict | list:
    """Try to parse JSON from AI response, handling markdown code blocks."""
    import re
    
    cleaned = text.strip()
    
    # First, try to extract JSON from markdown code blocks with proper newline handling
    code_block_match = re.search(r'```\s*(?:json)?\s*\n?(.*?)\n?```', cleaned, re.DOTALL)
    if code_block_match:
        block_content = code_block_match.group(1).strip()
        try:
            return json.loads(block_content)
        except (json.JSONDecodeError, ValueError):
            # If parsing fails, continue with cleaned block content
            cleaned = block_content
    
    # Try direct JSON parse on cleaned text
    try:
        return json.loads(cleaned)
    except (json.JSONDecodeError, ValueError):
        pass
    
    # Try to find JSON in text - look for { or [ patterns
    try:
        # Find first { or [ and try to parse from there
        brace_pos = cleaned.find('{')
        bracket_pos = cleaned.find('[')
        start_pos = -1
        
        if brace_pos >= 0 and bracket_pos >= 0:
            start_pos = min(brace_pos, bracket_pos)
        elif brace_pos >= 0:
            start_pos = brace_pos
        elif bracket_pos >= 0:
            start_pos = bracket_pos
        
        if start_pos >= 0:
            # Try to parse from the start position to the end
            for end_pos in range(len(cleaned), start_pos, -1):
                try:
                    return json.loads(cleaned[start_pos:end_pos])
                except (json.JSONDecodeError, ValueError):
                    continue
    except Exception:
        pass
    
    # Last resort - wrap the raw text as reasoning
    return {"reasoning": text}


def _generate_title(insight_type: str, data: dict) -> str:
    """Generate a human-readable title from insight data."""
    titles = {
        "demand_forecast": "Demand Forecast Analysis",
        "dead_stock": "Slow-Moving Item Detected",
        "anomaly": "Unusual Sales Pattern",
        "price_optimization": "Price Optimization Suggestion",
        "expiry_risk": "Stock Nearing Expiry",
        "stockout_prediction": "Stockout Risk Alert",
    }
    product_name = data.get("productName", data.get("name", ""))
    base_title = titles.get(insight_type, "AI Insight")
    if product_name:
        return f"{base_title}: {product_name}"
    return base_title


def _enrich_item_with_product(
    item: dict,
    products_by_id: dict[str, Product],
    products_by_sku: dict[str, Product],
    products_by_name: dict[str, Product],
) -> dict:
    """Attach productName when AI returns only productId/sku so UI text is clearer."""
    product_id = str(item.get("productId", ""))
    product_name = item.get("productName")
    product = None

    if product_id:
        product = products_by_id.get(product_id) or products_by_sku.get(product_id)

    if product is None and product_name:
        product = products_by_name.get(str(product_name).lower())

    if product:
        item["productName"] = product.name
        item["productId"] = str(product.id)
        item.setdefault("sku", product.sku)

        # Backfill pricing fields when AI returns null/None
        if item.get("currentPrice") in (None, "", "null"):
            item["currentPrice"] = product.sell_price
        if item.get("suggestedPrice") in (None, "", "null"):
            item["suggestedPrice"] = round(product.sell_price * 0.95, 2)

    elif not product_name and product_id:
        # Keep legacy behavior for unresolved IDs
        product = products_by_id.get(product_id) or products_by_sku.get(product_id)
        if product:
            item["productName"] = product.name
            item["productId"] = str(product.id)
            item.setdefault("sku", product.sku)

    return item


def _build_insight_description(data: dict, insight_type: str) -> str:
    """Build concise, project-grounded descriptions from structured fields."""
    if not isinstance(data, dict):
        return "AI-generated recommendation based on current inventory and sales patterns."

    product_name = data.get("productName") or "This product"

    if insight_type == "demand_forecast":
        predicted = data.get("predictedDemand", 0)
        stock = data.get("currentStock", 0)
        reorder = data.get("recommendedOrder", 0)
        confidence = data.get("confidence")
        confidence_text = f" Confidence: {confidence}%" if confidence is not None else ""
        return (
            f"{product_name}: predicted demand is {predicted} units, current stock is {stock}, "
            f"recommended reorder is {reorder} units.{confidence_text}"
        )
    if insight_type == "dead_stock":
        stock = data.get("currentStock", 0)
        avg_sales = data.get("averageMonthlySales", 0)
        discount = data.get("suggestedDiscount", 10)
        return (
            f"{product_name}: average monthly sales are {avg_sales} with current stock {stock}. "
            f"Suggested clearance discount is {discount}%."
        )
    if insight_type == "anomaly":
        normal = float(data.get("normalAverage", 0) or 0)
        current = float(data.get("currentSales", 0) or 0)
        raw_change = data.get("percentageChange")
        if raw_change in (None, "", "null"):
            change = ((current - normal) / normal * 100) if normal else 0
        else:
            change = float(raw_change)
        change_word = "increase" if current >= normal else "decrease"
        label = data.get("productName") or data.get("customer") or "Sales trend"
        label_norm = str(label).strip().lower()
        if label_norm in {"this product", "product", "unknown"} or label_norm.startswith("this product"):
            label = "Sales trend"
        return (
            f"{label}: detected {abs(change):.1f}% {change_word} versus baseline "
            f"({normal} to {current})."
        )
    if insight_type == "price_optimization":
        current_price = data.get("currentPrice", 0)
        if current_price in (None, "", "null", "None"):
            current_price = 0
        suggested_price = data.get("suggestedPrice")
        if suggested_price in (None, "", "null", "None"):
            suggested_price = current_price
        expected_revenue = data.get("expectedRevenue")
        revenue_text = f" Expected revenue: ₹{float(expected_revenue):,.0f}." if expected_revenue is not None else ""
        return (
            f"{product_name}: suggested price update from ₹{current_price} to ₹{suggested_price} to optimize margin and demand."
            f"{revenue_text}"
        )
    if insight_type == "expiry_risk":
        batch = data.get("batchNumber", "-")
        expiry = data.get("expiryDate", "-")
        units = data.get("unitsAtRisk", 0)
        action = data.get("suggestedAction")
        action_text = f" Recommended action: {action}." if action else ""
        return (
            f"{product_name}: batch {batch} expires on {expiry}; {units} units are at risk." 
            f"{action_text}"
        )

    return "AI-generated recommendation based on current inventory and sales patterns."


# ── New AI Features ──

def _get_sales_velocity(db: Session, product_id: int, days: int = 30) -> float:
    """Calculate average daily sales for a product over the given period."""
    since = datetime.now(timezone.utc) - timedelta(days=days)
    total_sold = (
        db.query(func.coalesce(func.sum(SaleItem.quantity), 0))
        .join(Sale, SaleItem.sale_id == Sale.id)
        .filter(
            SaleItem.product_id == product_id,
            Sale.status == "completed",
            Sale.date >= since,
        )
        .scalar()
    )
    return round(float(total_sold) / max(days, 1), 2)


def get_dashboard_summary(db: Session) -> DashboardSummaryResponse:
    """Generate a natural-language AI summary for the dashboard."""
    context = _build_inventory_context(db)
    prompt = dashboard_summary_prompt(context)
    summary = cerebras_client.complete(
        "You are a concise inventory management assistant. Respond in plain text only.",
        prompt,
    )
    return DashboardSummaryResponse(
        summary=summary,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )


def get_health_score(db: Session) -> HealthScoreResponse:
    """Calculate inventory health score (0-100) from real metrics + AI recommendation."""
    products = db.query(Product).all()
    total = len(products)
    if total == 0:
        return HealthScoreResponse(
            score=0, grade="F", breakdown={}, recommendation="No products found."
        )

    active = sum(1 for p in products if p.status == "active")
    low_stock = sum(1 for p in products if p.status == "low_stock")
    out_of_stock = sum(1 for p in products if p.status == "out_of_stock")

    # Stock adequacy: ratio of stock to min level, capped at 1
    adequacy_scores = []
    for p in products:
        if p.min_level and p.min_level > 0:
            adequacy_scores.append(min(p.stock_qty / p.min_level, 2.0) / 2.0)
        else:
            adequacy_scores.append(1.0 if p.stock_qty > 0 else 0.0)
    avg_adequacy = sum(adequacy_scores) / len(adequacy_scores) if adequacy_scores else 0

    # Revenue health: recent 30-day vs prior 30-day
    now = datetime.now(timezone.utc)
    rev_current = float(
        db.query(func.coalesce(func.sum(Sale.total_amount), 0))
        .filter(Sale.status == "completed", Sale.date >= now - timedelta(days=30))
        .scalar()
    )
    rev_previous = float(
        db.query(func.coalesce(func.sum(Sale.total_amount), 0))
        .filter(Sale.status == "completed", Sale.date >= now - timedelta(days=60), Sale.date < now - timedelta(days=30))
        .scalar()
    )
    rev_trend = min(rev_current / max(rev_previous, 1), 2.0) / 2.0  # 0-1 range

    # Weighted score
    availability_pct = active / total  # 0-1
    oos_penalty = out_of_stock / total  # 0-1, higher is worse
    low_penalty = low_stock / total * 0.5  # half weight

    score = int(round(
        (availability_pct * 30) +    # 30 pts for in-stock ratio
        (avg_adequacy * 30) +         # 30 pts for stock adequacy
        (rev_trend * 20) +            # 20 pts for revenue trend
        ((1 - oos_penalty) * 10) +    # 10 pts for no out-of-stock
        ((1 - low_penalty) * 10)      # 10 pts for no low-stock
    ))
    score = max(0, min(100, score))

    # Grade
    if score >= 90: grade = "A"
    elif score >= 80: grade = "B"
    elif score >= 70: grade = "C"
    elif score >= 60: grade = "D"
    else: grade = "F"

    breakdown = {
        "totalProducts": total,
        "activeProducts": active,
        "lowStockProducts": low_stock,
        "outOfStockProducts": out_of_stock,
        "stockAdequacy": round(avg_adequacy * 100, 1),
        "revenueTrend": round(rev_trend * 100, 1),
        "recentRevenue": round(rev_current, 2),
    }

    # AI recommendation
    metrics_json = json.dumps(breakdown, indent=2)
    prompt = health_score_prompt(metrics_json)
    recommendation = cerebras_client.complete(
        "You are an inventory health advisor. Respond in plain text only, 2-3 sentences.",
        prompt,
    )

    return HealthScoreResponse(
        score=score,
        grade=grade,
        breakdown=breakdown,
        recommendation=recommendation,
    )


def get_reorder_suggestions(db: Session) -> ReorderSuggestionsResponse:
    """AI-powered reorder suggestions for products running low."""
    products = db.query(Product).filter(
        Product.stock_qty <= Product.min_level * 1.5,
        Product.status.in_(["active", "low_stock", "out_of_stock"]),
    ).all()

    suggestions: list[ReorderSuggestion] = []
    product_context = []

    for p in products:
        daily_rate = _get_sales_velocity(db, p.id, 30)
        days_left = p.stock_qty / daily_rate if daily_rate > 0 else 999
        # Default suggestion: cover 30 days of demand + buffer to reach 2x min level
        base_qty = max(int(daily_rate * 30), p.min_level * 2) - p.stock_qty
        suggested_qty = max(base_qty, p.min_level)

        product_context.append({
            "productId": str(p.id),
            "name": p.name,
            "currentStock": p.stock_qty,
            "minLevel": p.min_level,
            "dailySalesRate": daily_rate,
            "daysUntilStockout": round(days_left, 1),
            "costPrice": p.cost_price,
            "defaultSuggestedQty": suggested_qty,
        })

    if product_context:
        # Get AI reasoning for each product
        try:
            raw = cerebras_client.complete(
                "You are an inventory reorder analyst. Respond only with valid JSON.",
                reorder_suggestion_prompt(json.dumps(product_context, indent=2)),
            )
            ai_data = _parse_ai_json(raw)
            ai_map = {}
            if isinstance(ai_data, list):
                for item in ai_data:
                    pid = str(item.get("productId", ""))
                    ai_map[pid] = item
        except Exception:
            ai_map = {}

        for ctx in product_context:
            ai_item = ai_map.get(ctx["productId"], {})
            suggestions.append(ReorderSuggestion(
                product_id=ctx["productId"],
                product_name=ctx["name"],
                current_stock=ctx["currentStock"],
                min_level=ctx["minLevel"],
                daily_sales_rate=ctx["dailySalesRate"],
                suggested_quantity=ai_item.get("suggestedQuantity", ctx["defaultSuggestedQty"]),
                days_until_stockout=ctx["daysUntilStockout"],
                reasoning=ai_item.get("reasoning", f"Stock is at {ctx['currentStock']} units with {ctx['dailySalesRate']} units/day sales rate."),
            ))

    return ReorderSuggestionsResponse(
        suggestions=suggestions,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )


def generate_report_narrative(db: Session, report_type: str, summary: dict) -> ReportNarrativeResponse:
    """Generate an AI narrative for a report."""
    prompt = report_narrative_prompt(report_type, json.dumps(summary, indent=2))
    narrative = cerebras_client.complete(
        "You are a business report writer. Respond in plain text only, 3-5 sentences.",
        prompt,
    )
    return ReportNarrativeResponse(
        narrative=narrative,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )


def get_stockout_predictions(db: Session) -> StockoutPredictionsResponse:
    """Predict which products will go out of stock and when."""
    products = db.query(Product).filter(Product.stock_qty > 0).all()
    predictions: list[StockoutPrediction] = []
    at_risk = []

    for p in products:
        daily_rate = _get_sales_velocity(db, p.id, 30)
        if daily_rate <= 0:
            continue
        days_left = round(p.stock_qty / daily_rate, 1)
        if days_left > 30:
            continue  # Not at risk

        if days_left <= 7:
            urgency = "critical"
        elif days_left <= 14:
            urgency = "warning"
        else:
            urgency = "watch"

        at_risk.append({
            "productId": str(p.id),
            "name": p.name,
            "currentStock": p.stock_qty,
            "dailySalesRate": daily_rate,
            "daysUntilStockout": days_left,
            "urgency": urgency,
        })

    # Get AI recommendations
    ai_rec_map = {}
    if at_risk:
        try:
            raw = cerebras_client.complete(
                "You are an inventory risk analyst. Respond only with valid JSON.",
                stockout_prediction_prompt(json.dumps(at_risk, indent=2)),
            )
            ai_data = _parse_ai_json(raw)
            if isinstance(ai_data, list):
                for item in ai_data:
                    ai_rec_map[str(item.get("productId", ""))] = item.get("recommendation", "")
        except Exception:
            pass

    for item in at_risk:
        pid = item["productId"]
        predictions.append(StockoutPrediction(
            product_id=pid,
            product_name=item["name"],
            current_stock=item["currentStock"],
            daily_sales_rate=item["dailySalesRate"],
            days_until_stockout=item["daysUntilStockout"],
            urgency=item["urgency"],
            recommendation=ai_rec_map.get(pid, f"Reorder {item['name']} soon - only {item['daysUntilStockout']} days of stock remaining."),
        ))

    # Sort by urgency
    urgency_order = {"critical": 0, "warning": 1, "watch": 2}
    predictions.sort(key=lambda p: (urgency_order.get(p.urgency, 3), p.days_until_stockout))

    return StockoutPredictionsResponse(
        predictions=predictions,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )


def get_sales_summary(db: Session) -> SalesSummaryResponse:
    """AI-generated sales trend analysis."""
    now = datetime.now(timezone.utc)

    periods = {
        "last7Days": (now - timedelta(days=7), now),
        "last30Days": (now - timedelta(days=30), now),
        "last90Days": (now - timedelta(days=90), now),
        "prior30Days": (now - timedelta(days=60), now - timedelta(days=30)),
    }

    metrics: dict = {}
    for label, (start, end) in periods.items():
        rev = float(
            db.query(func.coalesce(func.sum(Sale.total_amount), 0))
            .filter(Sale.status == "completed", Sale.date >= start, Sale.date < end)
            .scalar()
        )
        profit = float(
            db.query(func.coalesce(func.sum(Sale.profit), 0))
            .filter(Sale.status == "completed", Sale.date >= start, Sale.date < end)
            .scalar()
        )
        count = db.query(Sale).filter(Sale.status == "completed", Sale.date >= start, Sale.date < end).count()
        metrics[label] = {"revenue": round(rev, 2), "profit": round(profit, 2), "orders": count}

    # Top products last 30 days
    top_rows = (
        db.query(
            Product.name,
            func.sum(SaleItem.quantity).label("units"),
            func.sum(SaleItem.quantity * SaleItem.price).label("revenue"),
        )
        .join(SaleItem, SaleItem.product_id == Product.id)
        .join(Sale, SaleItem.sale_id == Sale.id)
        .filter(Sale.status == "completed", Sale.date >= now - timedelta(days=30))
        .group_by(Product.name)
        .order_by(func.sum(SaleItem.quantity * SaleItem.price).desc())
        .limit(5)
        .all()
    )
    metrics["topProducts"] = [
        {"name": r.name, "units": int(r.units), "revenue": round(float(r.revenue), 2)}
        for r in top_rows
    ]

    # Growth
    cur_rev = metrics["last30Days"]["revenue"]
    prev_rev = metrics["prior30Days"]["revenue"]
    growth = round((cur_rev - prev_rev) / prev_rev * 100, 1) if prev_rev > 0 else (100.0 if cur_rev > 0 else 0.0)
    metrics["growth30d"] = growth

    # AI summary
    prompt = sales_summary_prompt(json.dumps(metrics, indent=2))
    summary = cerebras_client.complete(
        "You are a sales analyst. Respond in plain text only, 3-4 sentences.",
        prompt,
    )

    return SalesSummaryResponse(
        summary=summary,
        metrics=metrics,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )
