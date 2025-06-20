# 📁 File: app/utils/offensive_filter.py
"""
Utility for optional offensive content filtering.
Can be toggled via config setting ENABLE_OFFENSIVE_CHECK.
"""

from better_profanity import profanity
from app.config import settings

# --- Config Toggle ---
def is_offensive_content_enabled() -> bool:
    return getattr(settings, "ENABLE_OFFENSIVE_CHECK", False)

# --- Content Check ---
def check_offensive_content(text: str) -> bool:
    """
    Returns True if offensive content is detected.
    """
    profanity.load_censor_words()
    return profanity.contains_profanity(text)
