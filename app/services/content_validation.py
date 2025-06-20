# 📁 File: app/services/content_validation.py
"""
Content validation utilities for content generation agent.
Ensures generated threads and articles meet user and platform constraints.
"""

import re

# --- Article Length Validation ---
def validate_article_length(text: str, max_words: int):
    """
    Raise ValueError if article exceeds word count limit.
    """
    word_count = len(re.findall(r"\w+", text))
    if word_count > max_words:
        raise ValueError(f"Generated article has {word_count} words, exceeds max {max_words}.")

# --- Thread Structure Validation ---
def validate_thread_structure(tweets: list[str], max_tweets: int, max_chars: int = 280) -> list[str]:
    """
    Ensures tweet count is within max_tweets.
    Allows tweets to exceed max_chars, but logs a warning (no truncation).
    """
    flagged = []
    trimmed = []

    for i, tweet in enumerate(tweets[:max_tweets]):
        tweet = tweet.strip()
        trimmed.append(tweet)
        if len(tweet) > max_chars:
            flagged.append((i, len(tweet)))

    if flagged:
        print(f"⚠️ Warning: Long tweets at positions {flagged}")

    return trimmed

