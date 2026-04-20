"""All ORM models — import this package to register them with SQLAlchemy."""

from .user import User
from .category import Category
from .supplier import Supplier
from .product import Product
from .warehouse import Warehouse, WarehouseStock
from .batch import Batch
from .purchase import Purchase, PurchaseItem
from .sale import Sale, SaleItem
from .alert import Alert
from .ai_prediction import AIPrediction

__all__ = [
    "User",
    "Category",
    "Supplier",
    "Product",
    "Warehouse",
    "WarehouseStock",
    "Batch",
    "Purchase",
    "PurchaseItem",
    "Sale",
    "SaleItem",
    "Alert",
    "AIPrediction",
]