"""Supplier routes — CRUD for /api/suppliers."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..models.supplier import Supplier
from ..auth.dependencies import get_current_user, require_permission
from ..repositories import supplier_repo
from ..schemas.supplier import SupplierResponse, SupplierCreate, SupplierUpdate
from ..schemas.base import camel_config

router = APIRouter(prefix="/api/suppliers", tags=["Suppliers"])


def _to_response(sup: Supplier) -> SupplierResponse:
    return SupplierResponse(
        id=sup.id,
        name=sup.name,
        contact_person=sup.contact_person,
        email=sup.email,
        phone=sup.phone,
        address=sup.address,
        city=sup.city,
        country=sup.country,
        products_supplied=sup.products_supplied,
        total_orders=sup.total_orders,
        total_value=sup.total_value,
        rating=sup.rating,
        status=sup.status,
        payment_terms=sup.payment_terms,
        created_at=str(sup.created_at)[:10] if sup.created_at else "",
    )


@router.get("", response_model=list[SupplierResponse])
def get_all_suppliers(
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("products.view")),
):
    suppliers = supplier_repo.get_all(db)
    return [_to_response(s) for s in suppliers]


@router.post("", response_model=SupplierResponse, status_code=201)
def create_supplier(
    data: SupplierCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    existing = supplier_repo.get_by_name(db, data.name)
    if existing:
        raise HTTPException(status_code=400, detail=f"Supplier '{data.name}' already exists")

    sup = Supplier(
        name=data.name,
        contact_person=data.contact_person,
        email=data.email,
        phone=data.phone,
        address=data.address,
        city=data.city,
        country=data.country,
        products_supplied=data.products_supplied,
        total_orders=data.total_orders,
        total_value=data.total_value,
        rating=data.rating,
        status=data.status,
        payment_terms=data.payment_terms,
    )
    sup = supplier_repo.create(db, sup)
    return _to_response(sup)


@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: str,
    data: SupplierUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    sup = supplier_repo.get_by_id(db, supplier_id)
    if not sup:
        raise HTTPException(status_code=404, detail="Supplier not found")

    updates = data.model_dump(exclude_unset=True)
    sup = supplier_repo.update(db, sup, updates)
    return _to_response(sup)


@router.delete("/{supplier_id}", status_code=204)
def delete_supplier(
    supplier_id: str,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    sup = supplier_repo.get_by_id(db, supplier_id)
    if not sup:
        raise HTTPException(status_code=404, detail="Supplier not found")
    supplier_repo.delete(db, sup)
