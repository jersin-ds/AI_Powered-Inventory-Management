"""Shared helpers for camelCase Pydantic models."""

from __future__ import annotations

from pydantic import ConfigDict


def to_camel(string: str) -> str:
    """Convert snake_case to camelCase."""
    parts = string.split("_")
    return parts[0] + "".join(w.capitalize() for w in parts[1:])


camel_config = ConfigDict(
    alias_generator=to_camel,
    populate_by_name=True,
    from_attributes=True,
)
