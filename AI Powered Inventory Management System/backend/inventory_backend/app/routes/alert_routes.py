"""Alert routes — /api/alerts."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..database import get_db
from ..models.alert import Alert
from ..models.user import User
from ..auth.dependencies import get_current_user

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])


class AlertResponse(BaseModel):
    id: str
    type: str
    title: str
    message: str
    priority: str
    read: bool
    created_at: str

    class Config:
        from_attributes = True


@router.get("", response_model=List[AlertResponse])
def get_alerts(
    unread_only: bool = False,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    """Return alerts, newest first. Optionally filter to unread only."""
    query = db.query(Alert)
    if unread_only:
        query = query.filter(Alert.read == False)  # noqa: E712
    alerts = query.order_by(Alert.created_at.desc()).all()
    results = []
    for a in alerts:
        results.append(AlertResponse(
            id=a.id,
            type=a.type,
            title=a.title,
            message=a.message,
            priority=a.priority,
            read=a.read,
            created_at=a.created_at.isoformat() if a.created_at else "",
        ))
    return results


@router.put("/{alert_id}/read")
def mark_alert_read(
    alert_id: str,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    """Mark a single alert as read."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.read = True
    db.commit()
    return {"detail": "Alert marked as read"}


@router.put("/read-all")
def mark_all_read(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    """Mark all alerts as read."""
    db.query(Alert).filter(Alert.read == False).update({"read": True})  # noqa: E712
    db.commit()
    return {"detail": "All alerts marked as read"}
