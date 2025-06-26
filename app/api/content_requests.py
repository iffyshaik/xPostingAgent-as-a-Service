# app/api/content_requests.py
"""
Submit new content generation requests (user topic, content type, etc.)
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.content_requests import CreateContentRequest, RequestListItem
from app.models.requests import Request
from typing import List


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


@router.get("", response_model=List[RequestListItem])
def get_user_requests(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """
    Fetch all content generation requests for the current user.
    """
    requests = db.query(Request).filter(Request.user_id == user_id).order_by(Request.created_at.desc()).all()
    return requests


from fastapi import Path
from app.models.research_sources import ResearchSource
from app.models.summaries import Summary
from app.models.content_queue import ContentQueue

@router.get("/{request_id}")
def get_request_detail(
    request_id: int = Path(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    """
    Returns full detail of a single request:
    topic, sources, summary, and content.
    """

    # Get request record
    request = db.query(Request).filter_by(id=request_id, user_id=user_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    # Get verified sources
    sources = db.query(ResearchSource).filter_by(
        request_id=request_id,
        user_id=user_id,
        verification_status="verified"
    ).all()

    source_data = [{
        "title": s.title,
        "url": s.url,
        "source_type": s.source_type,
        "relevance_score": s.relevance_score,
        "summary": s.summary,
        "key_points": s.key_points,
    } for s in sources]

    # Get summary
    summary = db.query(Summary).filter_by(request_id=request_id, user_id=user_id).first()

    # Get draft content
    content = db.query(ContentQueue).filter_by(request_id=request_id, user_id=user_id).first()

    return {
        "success": True,
        "data": {
            "request": {
                "id": request.id,
                "original_topic": request.original_topic,
                "content_topic": request.content_topic,
                "content_type": request.content_type,
                "status": request.status,
                "platform": request.platform,
                "created_at": request.created_at,
            },
            "sources": source_data,
            "summary": {
                "combined_summary": summary.combined_summary if summary else None,
                "key_points": summary.combined_key_points if summary else [],
            },
            "content": {
                "generated_content": content.generated_content if content else "",
                "status": content.status if content else "missing"
            }
        }
    }

