"""AI Prediction repository — DB operations for AI predictions/insights."""

from __future__ import annotations

from sqlalchemy.orm import Session

from ..models.ai_prediction import AIPrediction


def get_all(db: Session) -> list[AIPrediction]:
    return db.query(AIPrediction).order_by(AIPrediction.created_at.desc()).all()


def get_by_type(db: Session, insight_type: str) -> list[AIPrediction]:
    return (
        db.query(AIPrediction)
        .filter(AIPrediction.type == insight_type)
        .order_by(AIPrediction.created_at.desc())
        .all()
    )


def get_by_id(db: Session, prediction_id: str) -> AIPrediction | None:
    return db.query(AIPrediction).filter(AIPrediction.id == prediction_id).first()


def create(db: Session, prediction: AIPrediction) -> AIPrediction:
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


def delete_all(db: Session) -> None:
    db.query(AIPrediction).delete()
    db.commit()


def count(db: Session) -> int:
    return db.query(AIPrediction).count()
