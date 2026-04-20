"""Warehouse routes — CRUD for /api/warehouses."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..models.warehouse import Warehouse
from ..auth.dependencies import require_permission
from ..repositories import warehouse_repo
from ..schemas.warehouse import WarehouseResponse, WarehouseCreate, WarehouseUpdate

router = APIRouter(prefix="/api/warehouses", tags=["Warehouses"])


def _to_response(wh: Warehouse) -> WarehouseResponse:
    return WarehouseResponse(
        id=wh.id,
        name=wh.name,
        location=wh.location,
        capacity=wh.capacity,
        current_stock=wh.current_stock,
        manager=wh.manager,
        status=wh.status,
    )


@router.get("", response_model=list[WarehouseResponse])
def get_all_warehouses(
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("warehouses.view")),
):
    warehouses = warehouse_repo.get_all(db)
    return [_to_response(w) for w in warehouses]


@router.post("", response_model=WarehouseResponse, status_code=201)
def create_warehouse(
    data: WarehouseCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("warehouses.manage")),
):
    wh = Warehouse(
        name=data.name,
        location=data.location,
        capacity=data.capacity,
        current_stock=data.current_stock,
        manager=data.manager,
        status=data.status,
    )
    wh = warehouse_repo.create(db, wh)
    return _to_response(wh)


@router.put("/{warehouse_id}", response_model=WarehouseResponse)
def update_warehouse(
    warehouse_id: str,
    data: WarehouseUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("warehouses.manage")),
):
    wh = warehouse_repo.get_by_id(db, warehouse_id)
    if not wh:
        raise HTTPException(status_code=404, detail="Warehouse not found")

    updates = data.model_dump(exclude_unset=True)
    wh = warehouse_repo.update(db, wh, updates)
    return _to_response(wh)


@router.delete("/{warehouse_id}", status_code=204)
def delete_warehouse(
    warehouse_id: str,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("warehouses.manage")),
):
    wh = warehouse_repo.get_by_id(db, warehouse_id)
    if not wh:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    warehouse_repo.delete(db, wh)
