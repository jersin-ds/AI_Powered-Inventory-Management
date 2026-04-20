"""User repository — DB operations for users."""

from __future__ import annotations

from sqlalchemy.orm import Session

from ..models.user import User


def get_all(db: Session) -> list[User]:
    return db.query(User).order_by(User.created_at.desc()).all()


def get_by_id(db: Session, user_id: str) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(db: Session, user: User, updates: dict) -> User:
    for key, value in updates.items():
        if value is not None and hasattr(user, key):
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()


def count(db: Session) -> int:
    return db.query(User).count()


def count_by_role(db: Session, role: str) -> int:
    return db.query(User).filter(User.role == role).count()
