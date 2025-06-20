"""
Tests for content_agent.py including prompt building, validation, citation selection,
and offensive content filtering (configurable).
"""

import pytest
from types import SimpleNamespace

from app.agents.content_agent import (
    build_content_prompt,
    select_top_citations,
)
from app.services.content_validation import (
    validate_article_length,
    validate_thread_structure,
)
from app.utils.offensive_filter import check_offensive_content

# ------------------------
# Test 1: Prompt Generation
# ------------------------

def test_prompt_generation():
    summary = "AI is transforming education."
    key_points = ["Personalised learning", "AI tutors", "Data-driven feedback"]
    user_config = {
        "persona": "Friendly expert",
        "tone": "insightful",
        "style": "engaging",
        "language": "en"
    }
    prompt = build_content_prompt(summary, key_points, user_config, content_type="thread",tweet_count=5, article_length=1000,include_citations=False,citation_count=0,sources=[] )
    assert "Friendly expert" in prompt
    assert "insightful" in prompt
    assert "engaging" in prompt
    assert "AI is transforming education." in prompt

# ------------------------
# Test 2: Article Length Validation
# ------------------------

def test_article_length_validation_passes():
    content = " ".join(["word"] * 500)  # 500 words
    validate_article_length(content, max_words=1000)  # should not raise

def test_article_length_validation_fails():
    content = " ".join(["word"] * 1100)  # 1100 words
    with pytest.raises(ValueError):
        validate_article_length(content, max_words=1000)

# ------------------------
# Test 3: Thread Structure Validation
# ------------------------

def test_thread_structure_validation_passes():
    tweets = ["Short tweet", "Another short one"]
    validate_thread_structure(tweets, max_tweets=5,max_chars= 280)

def test_thread_structure_validation_flags_but_does_not_fail():
    tweets = ["x" * 300]
    result = validate_thread_structure(tweets, 5, 280)
    assert result[0] == tweets[0]

def test_thread_structure_validation_allows_long_tweets():
    tweet = "x" * 300
    result = validate_thread_structure([tweet], 5, 280)
    assert result[0] == tweet  # ensure tweet is not modified



# ------------------------
# Test 4: Citation Selection
# ------------------------

def test_select_top_citations():
    source1 = SimpleNamespace(title="A", relevance_score=0.9, freshness_score=0.8)
    source2 = SimpleNamespace(title="B", relevance_score=0.95, freshness_score=0.5)
    source3 = SimpleNamespace(title="C", relevance_score=0.7, freshness_score=0.9)
    top = select_top_citations([source1, source2, source3], max_count=2)
    assert len(top) == 2
    assert top[0].title == "B"  # highest relevance first

# ------------------------
# Test 5: Offensive Filter (Toggleable)
# ------------------------

def test_offensive_filter_detects_bad_word():
    text = "This is a damn test."  # Contains light profanity
    assert check_offensive_content(text) is True

def test_offensive_filter_skips_clean_text():
    text = "This is a wholesome sentence."
    assert check_offensive_content(text) is False
