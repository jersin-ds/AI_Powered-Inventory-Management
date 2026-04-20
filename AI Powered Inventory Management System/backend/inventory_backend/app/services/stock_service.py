"""Stock service — auto-reorder & stock adjustment logic."""

from __future__ import annotations

from datetime import datetime, timezone
from collections import defaultdict

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.product import Product
from ..models.purchase import Purchase, PurchaseItem
from ..repositories import product_repo, purchase_repo


def auto_reorder(db: Session, user_id: str) -> dict:
    """Scan low/out-of-stock products, group by supplier, create POs."""
    low = product_repo.get_low_stock(db)
    out = product_repo.get_out_of_stock(db)
    items = {p.id: p for p in [*low, *out]}  # dedupe by id

    if not items:
        return {"message": "All products are sufficiently stocked.", "orders_created": 0}

    # Group by supplier
    supplier_groups: dict[str, list[Product]] = defaultdict(list)
    for product in items.values():
        supplier_groups[product.supplier_id or "unknown"].append(product)

    orders_created = 0
    po_details = []
    po_counter = 0

    for supplier_id, products in supplier_groups.items():
        if supplier_id == "unknown":
            continue

        # Get a unique PO number for each supplier order
        base_po = purchase_repo.get_next_po_number(db)
        po_number = base_po if po_counter == 0 else f"{base_po}-{po_counter}"
        po_counter += 1
        total = 0.0
        po_items = []

        for p in products:
            # Order enough to reach double the minimum level
            qty_needed = max(p.min_level * 2 - p.stock_qty, p.min_level)
            item_total = qty_needed * p.cost_price
            total += item_total
            po_items.append(
                PurchaseItem(
                    product_id=p.id,
                    product_name=p.name,
                    quantity=qty_needed,
                    price=p.cost_price,
                )
            )

        purchase = Purchase(
            po_number=po_number,
            supplier_id=supplier_id,
            supplier_name=products[0].supplier_rel.name if products[0].supplier_rel else "Unknown",
            date=datetime.now(timezone.utc),
            status="pending",
            total_amount=round(total, 2),
            created_by=user_id,
        )
        purchase.items = po_items
        db.add(purchase)
        orders_created += 1
        po_details.append({
            "poNumber": po_number,
            "supplier": purchase.supplier_name,
            "items": len(po_items),
            "total": round(total, 2),
        })

    db.commit()

    return {
        "message": f"Created {orders_created} purchase order(s) for {len(items)} products.",
        "orders_created": orders_created,
        "orders": po_details,
    }


def adjust_stock(
    db: Session, product_id: str, quantity: int, reason: str, user_id: str
) -> dict:
    """Manually adjust stock by +/- quantity."""
    product = product_repo.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    old_qty = product.stock_qty
    product.stock_qty = max(0, product.stock_qty + quantity)
    product.sync_status()
    db.commit()

    return {
        "productId": product.id,
        "name": product.name,
        "previousQty": old_qty,
        "newQty": product.stock_qty,
        "adjustment": quantity,
        "reason": reason,
        "status": product.status,
    }
