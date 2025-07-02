"""
schema.py - Input and output models for the Content Planner Agent.

This file defines the Pydantic data structures used to:
1. Accept inputs into the planner agent (from API or internal usage)
2. Validate the structure of the agent's output before saving or passing on
3. Keep all contracts and typing in one place for clarity and maintainability

Pydantic is used because it's FastAPI's standard for data validation and documentation.
"""

from pydantic import BaseModel, Field
from typing import List, Literal

class PlannerSection(BaseModel):
    title: str = Field(..., description="Title of the content section")
    description: str = Field(..., description="Explanation of what to cover")
    suggested_support: str = Field(..., description="Suggested support material (e.g. quote, stat)")

class ContentPlannerOutput(BaseModel):
    framed_topic: str = Field(..., description="Refined version of original topic")
    content_angle: Literal[
        "commentary", "opinion", "case_study", "book_review", "how_to", "thought_experiment"
    ]
    structure_plan: List[PlannerSection]

class ContentPlannerInput(BaseModel):
    original_topic: str
    persona: str
    tone: str
    style: str
    content_type: Literal["thread", "article"]

