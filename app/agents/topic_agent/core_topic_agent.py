# app/agents/topic_agent.py

"""
This module handles the Topic Generation Agent logic.
It takes a user's original topic and configuration, builds a prompt, sends it to the LLM, and returns a focused content topic.
It also updates the database request row with the new topic and status.
"""

from app.prompts.topic_prompt import build_topic_prompt
from app.llm.engine import generate_completion
from app.database import SessionLocal
from app.models.requests import Request
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

def generate_content_topic(request_id: int, original_topic: str, user_config: dict, content_type: str, user_id: int) -> str:
    """
    Main logic for generating a refined content topic using user input and config.
    
    Args:
        request_id (int): ID of the request row in the DB
        original_topic (str): User's initial topic
        user_config (dict): Persona, tone, style, etc.
        content_type (str): 'thread' or 'article'
        user_id (int): ID of the user making the request

    Returns:
        str: Refined content topic
    """
    # Step 1: Build prompt
    prompt = build_topic_prompt(original_topic, user_config, content_type)

    # Step 2: Call LLM
    try:
        result = generate_completion(prompt)
        content_topic = result.strip()
    except Exception as e:
        logger.error(f"[TopicAgent] LLM failed for request_id={request_id}, user_id={user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate topic. Please try again.")

    # Step 3: Update DB
    db = SessionLocal()
    try:
        request = db.query(Request).filter_by(id=request_id, user_id=user_id).one()
        request.content_topic = content_topic
        request.status = "researching"
        db.commit()
    except NoResultFound:
        db.rollback()
        raise HTTPException(status_code=404, detail="Request not found.")
    except Exception as e:
        db.rollback()
        logger.error(f"[TopicAgent] DB update failed for request_id={request_id}, user_id={user_id}: {e}")
        raise HTTPException(status_code=500, detail="Could not update database with topic.")
    finally:
        db.close()

    return content_topic
