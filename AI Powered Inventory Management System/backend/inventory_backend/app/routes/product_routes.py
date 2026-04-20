"""Product routes — CRUD + search for /api/products."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..auth.dependencies import get_current_user, require_permission
from ..schemas.product import ProductResponse, ProductCreate, ProductUpdate
from ..services import product_service

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("/search", response_model=list[ProductResponse])
def search_products(
    q: str = Query("", description="Search query"),
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("products.view")),
):
    return product_service.search(db, q)


@router.get("", response_model=list[ProductResponse])
def get_all_products(
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("products.view")),
):
    return product_service.get_all(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: str,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("products.view")),
):
    return product_service.get_by_id(db, product_id)


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("products.create")),
):
    return product_service.create(db, data)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("products.edit")),
):
    return product_service.update(db, product_id, data)


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("products.delete")),
):
    product_service.delete(db, product_id)
