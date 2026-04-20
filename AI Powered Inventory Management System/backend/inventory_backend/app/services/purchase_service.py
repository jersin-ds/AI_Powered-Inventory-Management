"""Purchase service — business logic for purchase orders."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.purchase import Purchase, PurchaseItem
from ..models.product import Product
from ..repositories import purchase_repo, product_repo, supplier_repo
from ..schemas.purchase import PurchaseCreate, PurchaseResponse, PurchaseItemSchema


def _to_response(purchase: Purchase) -> PurchaseResponse:
    return PurchaseResponse(
        id=purchase.id,
        po_number=purchase.po_number,
        supplier=purchase.supplier_name or "",
        date=str(purchase.date)[:10] if purchase.date else "",
        status=purchase.status,
        total_amount=purchase.total_amount,
        items=[
            PurchaseItemSchema(
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                price=item.price,
            )
            for item in purchase.items
        ],
    )


def get_all(db: Session) -> list[PurchaseResponse]:
    purchases = purchase_repo.get_all(db)
    return [_to_response(p) for p in purchases]


def create(db: Session, data: PurchaseCreate, user_id: str | None = None) -> PurchaseResponse:
    # Resolve supplier
    supplier = supplier_repo.get_by_name(db, data.supplier)
    if not supplier:
        raise HTTPException(status_code=400, detail=f"Supplier '{data.supplier}' not found")

    po_number = purchase_repo.get_next_po_number(db)

    # Calculate total
    total = sum(item.quantity * item.price for item in data.items)

    # Parse date
    purchase_date = datetime.now(timezone.utc)
    if data.date:
        try:
            purchase_date = datetime.strptime(data.date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            pass

    purchase = Purchase(
        po_number=po_number,
        supplier_id=supplier.id,
        supplier_name=supplier.name,
        date=purchase_date,
        status=data.status,
        total_amount=total,
        created_by=user_id,
    )

    for item_data in data.items:
        purchase.items.append(
            PurchaseItem(
                product_id=item_data.product_id,
                product_name=item_data.product_name,
                quantity=item_data.quantity,
                price=item_data.price,
            )
        )

    purchase = purchase_repo.create(db, purchase)

    # Update supplier stats
    supplier.total_orders += 1
    supplier.total_value += total
    db.commit()

    return _to_response(purchase)


def update_status(db: Session, purchase_id: str, new_status: str) -> PurchaseResponse:
    purchase = purchase_repo.get_by_id(db, purchase_id)
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")

    old_status = purchase.status

    purchase = purchase_repo.update_status(db, purchase, new_status)

    # If marking as received, update product stock
    if new_status == "received" and old_status != "received":
        for item in purchase.items:
            product = product_repo.get_by_id(db, item.product_id)
            if product:
                product.stock_qty += item.quantity
                product.sync_status()
                db.commit()

    return _to_response(purchase)
