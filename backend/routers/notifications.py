"""
Notifications Router - Handles real-time notifications for students
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from database import get_db, Notification

router = APIRouter()


class NotificationCreate(BaseModel):
    title: str
    message: str
    category: str  # exam, placement, event, general
    target_branch: Optional[str] = "ALL"
    expires_at: Optional[datetime] = None


@router.get("/")
async def get_notifications(
    category: Optional[str] = None,
    branch: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all active notifications with optional filters"""
    query = db.query(Notification).filter(Notification.is_active == True)
    
    if category:
        query = query.filter(Notification.category == category)
    
    if branch:
        query = query.filter(
            (Notification.target_branch == "ALL") | 
            (Notification.target_branch == branch)
        )
    
    notifications = query.order_by(Notification.created_at.desc()).all()
    
    return [
        {
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "category": n.category,
            "target_branch": n.target_branch,
            "created_at": n.created_at.isoformat(),
        }
        for n in notifications
    ]


@router.post("/")
async def create_notification(notif: NotificationCreate, db: Session = Depends(get_db)):
    """Create a new notification (admin use)"""
    new_notif = Notification(
        title=notif.title,
        message=notif.message,
        category=notif.category,
        target_branch=notif.target_branch,
        expires_at=notif.expires_at
    )
    db.add(new_notif)
    db.commit()
    db.refresh(new_notif)
    return {"message": "Notification created", "id": new_notif.id}


@router.get("/categories")
async def get_categories():
    return {
        "categories": [
            {"id": "placement", "label": "Placement", "icon": "💼"},
            {"id": "exam", "label": "Examinations", "icon": "📝"},
            {"id": "event", "label": "Events", "icon": "🎉"},
            {"id": "general", "label": "General", "icon": "📢"},
        ]
    }
