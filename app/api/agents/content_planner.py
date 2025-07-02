"""
content_planner.py - API route for running the ContentPlannerAgent

This route accepts a user topic and preferences, runs the planner agent, and returns
the structured plan (framed topic, content angle, and content structure).
"""

from fastapi import APIRouter, Depends
from app.agents.content_planner_agent.agent import ContentPlannerAgent
from app.agents.content_planner_agent.schema import ContentPlannerInput, ContentPlannerOutput
from app.dependencies import get_current_user  # if you're using auth

router = APIRouter(prefix="/agents/content-planner", tags=["Content Planner"])

@router.post("/run", response_model=ContentPlannerOutput)
def run_planner(input_data: ContentPlannerInput):  # Add `user=Depends(get_current_user)` if needed
    agent = ContentPlannerAgent()
    output = agent.run(input_data)
    return output
