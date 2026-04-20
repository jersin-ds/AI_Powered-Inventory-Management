"""Product service — business logic for product CRUD and stock management."""

from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.product import Product
from ..models.category import Category
from ..models.supplier import Supplier
from ..repositories import product_repo, category_repo, supplier_repo
from ..schemas.product import ProductCreate, ProductUpdate, ProductResponse


def _resolve_category(db: Session, name: str) -> Category:
    cat = category_repo.get_by_name(db, name)
    if not cat:
        raise HTTPException(status_code=400, detail=f"Category '{name}' not found")
    return cat


def _resolve_supplier(db: Session, name: str) -> Supplier:
    sup = supplier_repo.get_by_name(db, name)
    if not sup:
        raise HTTPException(status_code=400, detail=f"Supplier '{name}' not found")
    return sup


def _to_response(product: Product) -> ProductResponse:
    cat_name = product.category_rel.name if product.category_rel else ""
    sup_name = product.supplier_rel.name if product.supplier_rel else ""
    return ProductResponse(
        id=product.id,
        sku=product.sku,
        name=product.name,
        category=cat_name,
        subcategory=product.subcategory,
        supplier=sup_name,
        cost_price=product.cost_price,
        sell_price=product.sell_price,
        stock_qty=product.stock_qty,
        min_level=product.min_level,
        barcode=product.barcode,
        image=product.image,
        status=product.status,
        created_at=str(product.created_at)[:10] if product.created_at else "",
    )


def get_all(db: Session) -> list[ProductResponse]:
    products = product_repo.get_all(db)
    return [_to_response(p) for p in products]


def get_by_id(db: Session, product_id: str) -> ProductResponse:
    product = product_repo.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return _to_response(product)


def create(db: Session, data: ProductCreate) -> ProductResponse:
    cat = _resolve_category(db, data.category)
    sup = _resolve_supplier(db, data.supplier)

    # Auto-generate SKU
    sku = data.sku
    if not sku:
        num = product_repo.get_next_sku_number(db)
        sku = f"SKU{num:03d}"

    # Check duplicate SKU
    if product_repo.get_by_sku(db, sku):
        raise HTTPException(status_code=400, detail=f"SKU '{sku}' already exists")

    product = Product(
        sku=sku,
        name=data.name,
        category_id=cat.id,
        subcategory=data.subcategory,
        supplier_id=sup.id,
        cost_price=data.cost_price,
        sell_price=data.sell_price,
        stock_qty=data.stock_qty,
        min_level=data.min_level,
        barcode=data.barcode,
        image=data.image,
    )
    product.sync_status()
    product = product_repo.create(db, product)

    # Update category product count
    cat.product_count = product_repo.count_by_category(db, cat.id)
    db.commit()

    return _to_response(product)


def update(db: Session, product_id: str, data: ProductUpdate) -> ProductResponse:
    product = product_repo.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    updates: dict = {}
    if data.name is not None:
        updates["name"] = data.name
    if data.subcategory is not None:
        updates["subcategory"] = data.subcategory
    if data.cost_price is not None:
        updates["cost_price"] = data.cost_price
    if data.sell_price is not None:
        updates["sell_price"] = data.sell_price
    if data.stock_qty is not None:
        updates["stock_qty"] = data.stock_qty
    if data.min_level is not None:
        updates["min_level"] = data.min_level
    if data.barcode is not None:
        updates["barcode"] = data.barcode
    if data.image is not None:
        updates["image"] = data.image

    if data.category is not None:
        cat = _resolve_category(db, data.category)
        updates["category_id"] = cat.id
    if data.supplier is not None:
        sup = _resolve_supplier(db, data.supplier)
        updates["supplier_id"] = sup.id

    product = product_repo.update(db, product, updates)
    return _to_response(product)


def delete(db: Session, product_id: str) -> None:
    product = product_repo.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    old_cat_id = product.category_id
    product_repo.delete(db, product)

    # Update category product count
    cat = category_repo.get_by_id(db, old_cat_id)
    if cat:
        cat.product_count = product_repo.count_by_category(db, old_cat_id)
        db.commit()


def search(db: Session, query: str) -> list[ProductResponse]:
    products = product_repo.search(db, query)
    return [_to_response(p) for p in products]


def get_low_stock(db: Session) -> list[ProductResponse]:
    products = product_repo.get_low_stock(db)
    return [_to_response(p) for p in products]


def get_out_of_stock(db: Session) -> list[ProductResponse]:
    products = product_repo.get_out_of_stock(db)
    return [_to_response(p) for p in products]
