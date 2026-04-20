"""Sale service — business logic for sales / invoices."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.sale import Sale, SaleItem
from ..repositories import sale_repo, product_repo
from ..schemas.sale import SaleCreate, SaleResponse, SaleItemSchema


def _to_response(sale: Sale) -> SaleResponse:
    return SaleResponse(
        id=sale.id,
        invoice_number=sale.invoice_number,
        customer=sale.customer,
        date=str(sale.date)[:10] if sale.date else "",
        status=sale.status,
        total_amount=sale.total_amount,
        profit=sale.profit,
        items=[
            SaleItemSchema(
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                price=item.price,
            )
            for item in sale.items
        ],
    )


def get_all(db: Session) -> list[SaleResponse]:
    sales = sale_repo.get_all(db)
    return [_to_response(s) for s in sales]


def create(db: Session, data: SaleCreate, user_id: str | None = None) -> SaleResponse:
    invoice_number = sale_repo.get_next_invoice_number(db)

    # Parse date
    sale_date = datetime.now(timezone.utc)
    if data.date:
        try:
            sale_date = datetime.strptime(data.date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            pass

    total_amount = 0.0
    total_profit = 0.0

    sale = Sale(
        invoice_number=invoice_number,
        customer=data.customer,
        date=sale_date,
        status=data.status,
        created_by=user_id,
    )

    for item_data in data.items:
        product = product_repo.get_by_id(db, item_data.product_id)
        if not product:
            raise HTTPException(status_code=400, detail=f"Product '{item_data.product_id}' not found")

        # Check stock
        if product.stock_qty < item_data.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for '{product.name}': available {product.stock_qty}, requested {item_data.quantity}",
            )

        line_total = item_data.quantity * item_data.price
        line_profit = (item_data.price - product.cost_price) * item_data.quantity

        total_amount += line_total
        total_profit += line_profit

        sale.items.append(
            SaleItem(
                product_id=item_data.product_id,
                product_name=item_data.product_name or product.name,
                quantity=item_data.quantity,
                price=item_data.price,
            )
        )

        # Deduct stock
        product.stock_qty -= item_data.quantity
        product.sync_status()

    sale.total_amount = total_amount
    sale.profit = total_profit

    sale = sale_repo.create(db, sale)
    return _to_response(sale)


def update_status(db: Session, sale_id: str, new_status: str) -> SaleResponse:
    sale = sale_repo.get_by_id(db, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    sale.status = new_status
    db.commit()
    db.refresh(sale)
    return _to_response(sale)
