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
    return approve_content(content_id=content_id, db=db)


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


