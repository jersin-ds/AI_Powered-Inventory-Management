"""Utility helpers for the inventory backend."""

from __future__ import annotations

import uuid


def generate_id() -> str:
    """Generate a UUID4 string."""
    return str(uuid.uuid4())


def generate_sku(sequence: int) -> str:
    """Generate SKU like SKU001, SKU002, etc."""
    return f"SKU{sequence:03d}"


def generate_po_number(year: int, sequence: int) -> str:
    """Generate PO number like PO-2024-001."""
    return f"PO-{year}-{sequence:03d}"


def generate_invoice_number(year: int, sequence: int) -> str:
    """Generate invoice number like INV-2024-001."""
    return f"INV-{year}-{sequence:03d}"
