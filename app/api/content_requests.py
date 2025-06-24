# app/api/content_requests.py
"""
Submit new content generation requests (user topic, content type, etc.)
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.content_requests import CreateContentRequest
from app.models.requests import Request

router = APIRouter(prefix="/content/requests", tags=["Content Requests"])

@router.post("")
def submit_content_request(
    payload: CreateContentRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """
    Creates a new content generation request.
    """
    new_request = Request(
        user_id=user_id,
        original_topic=payload.original_topic,
        content_type=payload.content_type,
        auto_post=payload.auto_post,
        thread_tweet_count=payload.thread_tweet_count,
        max_article_length=payload.max_article_length,
        include_source_citations=payload.include_source_citations,
        citation_count=payload.citation_count,
        platform=payload.platform
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return {
        "success": True,
        "request_id": new_request.id,
        "message": "Topic submitted successfully"
    }
