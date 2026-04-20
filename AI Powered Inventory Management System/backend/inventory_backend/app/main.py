"""
AI-Powered Inventory Management System — FastAPI Backend

Start with:
    uvicorn inventory_backend.app.main:app --reload --port 8000
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import engine, Base

# Import all models so they are registered with SQLAlchemy
from .models import (  # noqa: F401
    User, Category, Supplier, Product,
    Warehouse, WarehouseStock, Batch,
    Purchase, PurchaseItem, Sale, SaleItem,
    Alert, AIPrediction,
)

from .middleware.logging import LoggingMiddleware

# Import all route modules
from .routes import (
    auth_routes,
    product_routes,
    category_routes,
    supplier_routes,
    warehouse_routes,
    stock_routes,
    purchase_routes,
    sale_routes,
    user_routes,
    dashboard_routes,
    report_routes,
    analytics_routes,
    ai_routes,
    alert_routes,
)

# ── Logging ──
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(name)s │ %(message)s",
)
logger = logging.getLogger("inventory_backend")


# ── Lifespan ──
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating database tables …")
    Base.metadata.create_all(bind=engine)
    logger.info("Database ready ✓")
    yield
    logger.info("Shutting down …")


# ── Application ──
app = FastAPI(
    title="AI-Powered Inventory Management System",
    description="Backend API for the inventory management system with Cerebras AI integration.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── Middleware ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

# ── Routes ──
app.include_router(auth_routes.router)
app.include_router(product_routes.router)
app.include_router(category_routes.router)
app.include_router(supplier_routes.router)
app.include_router(warehouse_routes.router)
app.include_router(stock_routes.router)
app.include_router(purchase_routes.router)
app.include_router(sale_routes.router)
app.include_router(user_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(report_routes.router)
app.include_router(analytics_routes.router)
app.include_router(ai_routes.router)
app.include_router(alert_routes.router)


# ── Health check ──
@app.get("/api/health", tags=["Health"])
def health():
    return {"status": "ok", "service": "inventory-backend"}


# ── Run directly ──
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "inventory_backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
