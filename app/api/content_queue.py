# app/api/content_queue.py
"""
Routes for managing content lifecycle:
- Approve draft content
- Schedule approved content
- Post content (simulated)

These call the business logic in app/services/content_queue.py
"""

from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session
from datetime import datetime
from app.services.content_queue import delete_scheduled_content

from app.dependencies import get_db, get_current_user
from app.services.content_queue import (
    approve_content,
    schedule_content,
    post_content,
)

# Define the router for this module
router = APIRouter(prefix="/content/queue", tags=["Content Queue"])


@router.put("/{content_id}/approve")
def approve_content_route(
    content_id: int = Path(..., description="ID of content to approve"),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    """
    Validates and approves draft content.
    """
    approve_content(content_id=content_id, db=db)
    post_content(content_id, db)

    return {"success": True} #approve_content(content_id=content_id, db=db)


@router.put("/{content_id}/schedule")
def schedule_content_route(
    content_id: int = Path(..., description="ID of content to schedule"),
    scheduled_for: datetime = Body(..., embed=True),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    """
    Schedules content to be posted later.
    """
    return schedule_content(content_id=content_id, scheduled_for=scheduled_for, db=db)


@router.post("/{content_id}/post")
def post_content_route(
    content_id: int = Path(..., description="ID of content to post"),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    """
    Simulates immediate posting of content.
    """
    return post_content(content_id=content_id, db=db)

@router.delete("/{content_id}")
def delete_scheduled_content_route(
    content_id: int = Path(..., description="ID of scheduled content to delete"),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return delete_scheduled_content(content_id=content_id, db=db)

@router.get("/scheduled")
def get_scheduled_content(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """
    Return all scheduled or previously scheduled-and-deleted posts.
    """
    from app.models.content_queue import ContentQueue

    results = db.query(ContentQueue).filter(
        ContentQueue.user_id == user_id,
        ContentQueue.status.in_(["scheduled", "scheduled_deleted"])
    ).order_by(ContentQueue.scheduled_for.asc()).all()

    return {
        "success": True,
        "data": [
            {
                "id": c.id,
                "content_type": c.content_type,
                "status": c.status,
                "scheduled_for": c.scheduled_for,
                "deleted_at": c.deleted_at,
                "platform": c.platform,
                "generated_content": c.generated_content,
            } for c in results
        ]
    }


