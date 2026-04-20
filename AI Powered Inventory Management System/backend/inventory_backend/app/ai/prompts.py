"""Structured prompts for AI features."""

from __future__ import annotations


INVENTORY_SYSTEM_PROMPT = """You are an AI assistant EXCLUSIVELY for an inventory management system.
You have access to real-time inventory data and can provide actionable insights.

STRICT SCOPE RULES — YOU MUST FOLLOW THESE:
- You ONLY answer questions related to inventory, stock, products, sales, purchases, suppliers, warehouses, categories, pricing, demand, forecasting, and business analytics within this inventory system.
- If the user asks about ANYTHING outside of inventory management (e.g. general knowledge, coding, weather, news, personal advice, jokes, stories, math homework, recipes, travel, politics, health, entertainment, or any other non-inventory topic), you MUST politely refuse.
- When refusing, say: "I can only help with inventory-related questions such as stock levels, sales data, product details, reorder suggestions, and business analytics. Please ask me something about your inventory!"
- NEVER answer general knowledge questions, even if the user insists.
- NEVER generate code, stories, poems, or any content unrelated to this inventory system.

RESPONSE RULES:
- Keep responses SHORT (2-4 sentences max).
- Do NOT use markdown formatting like ** or ## or bullet lists.
- Use plain text only. No bold, no headers, no code blocks.
- Be concise and direct. Give a brief summary, not a detailed listing.
- When discussing numbers, be precise but brief.
- All monetary values are in Indian Rupees (INR/₹). Always use ₹ symbol, never $.
- Never list out all products; summarize instead."""


def chat_system_prompt(context: str) -> str:
    return f"""{INVENTORY_SYSTEM_PROMPT}

Here is the current inventory context data:
{context}

Use this data to answer the user's questions accurately. If the user asks about specific
products, reference the actual data. Provide actionable recommendations when relevant.

REMINDER: If the user asks anything NOT related to this inventory data or inventory management
in general, politely decline and redirect them to ask inventory-related questions instead.
Do NOT answer general knowledge, coding, math, science, or any off-topic questions."""


def demand_forecast_prompt(product_data: str) -> str:
    return f"""Analyze the following product sales data and provide a demand forecast.

Product Data:
{product_data}

Respond in JSON format with these fields:
- productId: string
- predictedDemand: number (units expected in next 2 weeks)
- currentStock: number
- recommendedOrder: number (units to order)
- confidence: number (0-100)
- reasoning: string (brief explanation)

Return ONLY a valid JSON array with maximum 3 items.
No markdown, no code fences, no extra text."""


def dead_stock_prompt(product_data: str) -> str:
    return f"""Analyze inventory for slow-moving or dead stock items.

Product Data:
{product_data}

Identify products with low sales velocity relative to current stock.
Suggest discount percentages to move inventory.

Respond in JSON format with these fields per item:
- productId: string
- averageMonthlySales: number
- currentStock: number
- suggestedDiscount: number (percentage)
- reasoning: string

Return ONLY a valid JSON array with maximum 3 items.
No markdown, no code fences, no extra text."""


def anomaly_detection_prompt(sales_data: str) -> str:
    return f"""Analyze sales patterns for anomalies or unusual trends.

Sales Data:
{sales_data}

Identify any unusual spikes, drops, or patterns.

Respond in JSON format with these fields per anomaly:
- productId: string
- normalAverage: number
- currentSales: number
- percentageChange: number
- type: string (spike/drop/trend)
- reasoning: string

Return ONLY a valid JSON array with maximum 3 items.
No markdown, no code fences, no extra text."""


def price_optimization_prompt(product_data: str) -> str:
    return f"""Analyze product pricing for optimization opportunities.

Product Data:
{product_data}

Consider cost prices, current sell prices, margins, and demand levels.

Respond ONLY with a JSON array of suggestions. Each suggestion must have:
- productId: string
- currentPrice: number or null
- suggestedPrice: number
- expectedRevenue: number
- reasoning: string

Example format:
[
    {{"productId": "1", "currentPrice": 2000, "suggestedPrice": 1800, "expectedRevenue": 180000, "reasoning": "..."}}
]

Return ONLY a valid JSON array with maximum 3 items.
No markdown, no code fences, no extra text."""


def expiry_risk_prompt(batch_data: str) -> str:
    return f"""Analyze product batches for expiry risk.

Batch Data:
{batch_data}

Identify items nearing expiry and suggest actions.

Respond in JSON format with these fields per risk:
- productId: string
- batchNumber: string
- expiryDate: string
- unitsAtRisk: number
- suggestedAction: string

Return ONLY a valid JSON array with maximum 3 items.
No markdown, no code fences, no extra text."""


# ── New AI Feature Prompts ──

def dashboard_summary_prompt(context: str) -> str:
    return f"""You are an inventory management AI assistant.
Analyze the following inventory data and write a brief executive summary for a business owner.

{context}

RULES:
- Write exactly 3-4 sentences in plain text.
- Highlight the most important numbers (revenue, profit, alerts).
- Mention any urgent issues (low stock, out of stock).
- End with one actionable recommendation.
- Use ₹ for all monetary values. No markdown, no bullet lists, no bold text."""


def health_score_prompt(metrics_json: str) -> str:
    return f"""You are an inventory health analyst. Based on these metrics, provide a brief recommendation.

Metrics:
{metrics_json}

RULES:
- Write exactly 2-3 sentences of plain text recommendation.
- Focus on the most critical issue.
- Suggest one specific action to improve inventory health.
- Use ₹ for monetary values. No markdown formatting."""


def reorder_suggestion_prompt(product_data: str) -> str:
    return f"""Analyze these products that are running low and suggest optimal reorder quantities.

Product Data:
{product_data}

For each product, consider:
- Current stock vs minimum level
- Daily sales rate (units/day)  
- Lead time assumption of 7 days

Respond in JSON array format with these fields per product:
- productId: string
- suggestedQuantity: number (units to order)
- reasoning: string (1 sentence explaining why)

Return ONLY a JSON array, no other text."""


def report_narrative_prompt(report_type: str, summary_json: str) -> str:
    return f"""Write a brief executive summary for this {report_type} report.

Report Summary Data:
{summary_json}

RULES:
- Write exactly 3-5 sentences in plain text.
- Highlight key numbers and trends.
- Compare performance indicators.
- End with a forward-looking statement.
- Use ₹ for monetary values. No markdown formatting."""


def stockout_prediction_prompt(product_data: str) -> str:
    return f"""Analyze these products and predict stockout risks.

Product Data with Sales Velocity:
{product_data}

For each product at risk, provide a brief recommendation.

Respond in JSON array format with these fields per product:
- productId: string
- recommendation: string (1 sentence action item)

Return ONLY a JSON array, no other text."""


def sales_summary_prompt(sales_data: str) -> str:
    return f"""Analyze these sales metrics and write a trend analysis.

Sales Data:
{sales_data}

RULES:
- Write exactly 3-4 sentences in plain text.
- Compare recent vs historical performance.
- Identify the strongest and weakest areas.
- Suggest one action based on the trends.
- Use ₹ for monetary values. No markdown formatting."""
