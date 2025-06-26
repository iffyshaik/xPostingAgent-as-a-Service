# app/schemas/content_requests.py
"""
Pydantic schema for submitting a new content generation request.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal

class CreateContentRequest(BaseModel):
    original_topic: str = Field(..., example="AI and the future of education")
    content_type: Literal["thread", "article"] = Field(..., example="thread")
    auto_post: Optional[bool] = False
    thread_tweet_count: Optional[int] = 5
    max_article_length: Optional[int] = 1000
    include_source_citations: Optional[bool] = True
    citation_count: Optional[int] = 2
    platform: Literal["x", "typefully"] = "typefully"



from datetime import datetime

class RequestListItem(BaseModel):
    id: int
    original_topic: str
    content_topic: Optional[str]
    content_type: str
    status: str
    platform: str
    created_at: datetime

    class Config:
        orm_mode = True

