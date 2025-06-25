# app/schemas/user_configurations.py

from pydantic import BaseModel
from typing import Optional

class UpdateUserConfig(BaseModel):
    persona: Optional[str] = None
    tone: Optional[str] = None
    style: Optional[str] = None
    language: Optional[str] = None
    platform_preference: Optional[str] = None
    research_preference: Optional[str] = None
