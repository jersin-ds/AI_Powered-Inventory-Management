"""Category repository — DB operations for categories."""

from __future__ import annotations

from sqlalchemy.orm import Session

from ..models.category import Category


def get_all(db: Session) -> list[Category]:
    return db.query(Category).order_by(Category.name).all()


def get_by_id(db: Session, category_id: str) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()


def get_by_name(db: Session, name: str) -> Category | None:
    return db.query(Category).filter(Category.name == name).first()


def create(db: Session, category: Category) -> Category:
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update(db: Session, category: Category, updates: dict) -> Category:
    for key, value in updates.items():
        if value is not None and hasattr(category, key):
            setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category


def delete(db: Session, category: Category) -> None:
    db.delete(category)
    db.commit()


def count(db: Session) -> int:
    return db.query(Category).count()
