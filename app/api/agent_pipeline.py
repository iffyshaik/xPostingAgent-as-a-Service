# app/api/agent_pipeline.py
"""
Routes to manually run each agent (Topic, Research, Summary, Content) step-by-step.
This allows testing the full pipeline through Swagger.
"""

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.agents.topic_agent.core_topic_agent import generate_content_topic
from app.agents.research_agent.core_research_agent import generate_research_sources
from app.agents.summary_agent.core_summary_agent import generate_and_store_summary
from app.agents.content_agent.core_content_agent import create_content
from app.models.requests import Request
from app.models.user_configurations import UserConfiguration
from app.models.research_sources import ResearchSource
from app.models.summaries import Summary

router = APIRouter(prefix="/pipeline", tags=["Pipeline Agents"])

@router.post("/{request_id}/topic")
def run_topic_agent(
    request_id: int = Path(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """
    Run Topic Agent to refine the original topic.
    """
    request = db.query(Request).filter_by(id=request_id, user_id=user_id).first()
    config = db.query(UserConfiguration).filter_by(user_id=user_id).first()

    config_dict = {
        "persona": config.persona,
        "tone": config.tone,
        "style": config.style,
        "language": config.language,
    }

    content_topic = generate_content_topic(
        request_id,
        request.original_topic,
        config_dict,
        request.content_type,
        user_id
    )
    return {"success": True, "refined_topic": content_topic}


@router.post("/{request_id}/research")
def run_research_agent(
    request_id: int = Path(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """
    Run Research Agent to find and verify sources.
    """
    request = db.query(Request).filter_by(id=request_id, user_id=user_id).first()
    config = db.query(UserConfiguration).filter_by(user_id=user_id).first()

    success = generate_research_sources(
        request_id,
        request.content_topic,
        user_id,
        limit=config.default_source_count,
        preference=config.research_preference
    )
    return {"success": success}


@router.post("/{request_id}/summary")
def run_summary_agent(
    request_id: int = Path(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """
    Run Summary Agent to generate a combined summary from verified sources.
    """
    request = db.query(Request).filter_by(id=request_id, user_id=user_id).first()

    verified_sources = db.query(ResearchSource).filter_by(
        request_id=request_id,
        verification_status="verified"
    ).filter(ResearchSource.summary.isnot(None)).all()

    if not verified_sources:
        return {"success": False, "error": "No verified sources with summaries."}

    source_data = [
        {
            "summary": src.summary,
            "key_points": src.key_points if isinstance(src.key_points, list) else []
        } for src in verified_sources
    ]

    summary_obj=generate_and_store_summary(
        request_id=request_id,
        verified_sources=source_data,
        target_length=500,
        content_type=request.content_type,
        user_id=user_id
    )
    if summary_obj is None:
        return {"success": False, "error": "No valid sources found to generate summary."}

    return {"success": True, "summary_id": summary_obj.id}

    


@router.post("/{request_id}/content")
def run_content_agent(
    request_id: int = Path(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """
    Run Content Agent to generate thread or article from summary.
    """
    request = db.query(Request).filter_by(id=request_id, user_id=user_id).first()
    config = db.query(UserConfiguration).filter_by(user_id=user_id).first()
    summary = db.query(Summary).filter_by(request_id=request_id).first()
    if not summary:
        raise HTTPException(status_code=400, detail="No summary found for this request")
    sources = db.query(ResearchSource).filter_by(
        request_id=request_id,
        verification_status="verified"
    ).all()

    config_dict = {
        "persona": config.persona,
        "tone": config.tone,
        "style": config.style,
        "language": config.language,
    }

    result = create_content(db, request, summary, sources, config_dict)
    return {"success": True, "content_id": result.id}
