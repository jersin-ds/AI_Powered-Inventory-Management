"""Category routes — CRUD for /api/categories."""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..models.category import Category
from ..auth.dependencies import get_current_user, require_permission
from ..repositories import category_repo, product_repo
from ..schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/api/categories", tags=["Categories"])


def _to_response(cat: Category) -> CategoryResponse:
    return CategoryResponse(
        id=cat.id,
        name=cat.name,
        description=cat.description,
        product_count=cat.product_count,
        subcategories=cat.get_subcategories(),
        status=cat.status,
        created_at=str(cat.created_at)[:10] if cat.created_at else "",
    )


@router.get("", response_model=list[CategoryResponse])
def get_all_categories(
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("products.view")),
):
    categories = category_repo.get_all(db)
    return [_to_response(c) for c in categories]


@router.post("", response_model=CategoryResponse, status_code=201)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    existing = category_repo.get_by_name(db, data.name)
    if existing:
        raise HTTPException(status_code=400, detail=f"Category '{data.name}' already exists")

    cat = Category(
        name=data.name,
        description=data.description,
        subcategories=json.dumps(data.subcategories),
        status=data.status,
    )
    cat = category_repo.create(db, cat)
    return _to_response(cat)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: str,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    cat = category_repo.get_by_id(db, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    updates: dict = {}
    if data.name is not None:
        updates["name"] = data.name
    if data.description is not None:
        updates["description"] = data.description
    if data.subcategories is not None:
        updates["subcategories"] = json.dumps(data.subcategories)
    if data.status is not None:
        updates["status"] = data.status

    cat = category_repo.update(db, cat, updates)

    # Recount products
    cat.product_count = product_repo.count_by_category(db, cat.id)
    db.commit()

    return _to_response(cat)


@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: str,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    cat = category_repo.get_by_id(db, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    # Check if category has products
    count = product_repo.count_by_category(db, category_id)
    if count > 0:
        raise HTTPException(status_code=400, detail=f"Cannot delete: category has {count} products")

    category_repo.delete(db, cat)
