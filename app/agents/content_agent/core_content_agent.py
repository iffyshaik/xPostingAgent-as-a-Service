# 📁 File: app/agents/content_agent.py
"""
Content Agent (Phase 4):
Generates social media content (thread/article) from combined summary and key points,
using user configurations and request parameters.
"""

import datetime
from app.llm.engine import generate_completion
from app.config import settings
from app.models.research_sources import ResearchSource
from app.models.content_queue import ContentQueue
from app.models.thread_metadata import ThreadMetadata
from app.services.content_validation import validate_thread_structure, validate_article_length
from app.utils.offensive_filter import is_offensive_content_enabled, check_offensive_content
from sqlalchemy.orm import Session

# --- Core Function ---
def create_content(
    db: Session,
    request,
    summary,
    research_sources: list[ResearchSource],
    user_config: dict
):
    """
    Generate content using LLM and save to content_queue (+ thread_metadata if thread).
    """
    if not summary or not summary.combined_summary:
        raise ValueError("Missing summary content. Cannot generate post.")
    
    prompt = build_content_prompt(
        request.content_topic,
        summary.combined_summary,
        summary.combined_key_points,
        user_config,
        request.content_type,
        request.thread_tweet_count,
        request.max_article_length,
        request.include_source_citations,
        request.citation_count,
        research_sources,
        # request.max_tweet_length  # <-- Enable this once added to model
    )

    llm_output = generate_completion(prompt, agent="content_agent")
    print("This is the twwet generation LLM output: \n{llm_output}")

    # Optional: Validate structure
    if request.content_type == "thread":
        print(f"🔎 LLM output before splitting:\n{llm_output}\n")

        tweets = split_into_tweets(llm_output, request.thread_tweet_count)
        print(f"🧵 Total tweets after splitting: {len(tweets)}")
        #tweets = [f"{i+1}/{len(tweets)}  \n{t}" for i, t in enumerate(tweets)]

        cleaned_tweets = clean_split_tweets(tweets)
        joined_thread = join_tweets_for_platform(cleaned_tweets, platform=request.platform)

        for i, t in enumerate(tweets):
            print(f"Tweet {i+1} ({len(t)} chars): {t}\n")

        tweets = validate_thread_structure(tweets, request.thread_tweet_count)
    else:
        validate_article_length(llm_output, request.max_article_length)

    # Optional: Offensive content check
    if is_offensive_content_enabled() and check_offensive_content(llm_output):
        content_status = "flagged"
    else:
        content_status = "draft"
    #joined_thread="\n\n".join(tweets)
    # Save content to content_queue
    new_content = ContentQueue(
        request_id=request.id,
        user_id=request.user_id,
        content_type=request.content_type,
        generated_content=joined_thread, #llm_output,
        status=content_status,
        scheduled_for=None,
        platform=request.platform,
        created_at=datetime.datetime.utcnow(),
    )
    db.add(new_content)
    db.flush()  # to get content_id for FK use

    # If thread, save metadata
    if request.content_type == "thread":
        thread_meta = ThreadMetadata(
            content_queue_id=new_content.id,
            requested_tweet_count=request.thread_tweet_count,
            actual_tweet_count=len(tweets),
            max_tweet_length=280,  # request.max_tweet_length (uncomment after model update)
            thread_structure=[{"tweet": t} for t in tweets],
            citation_tweets=[],
            created_at=datetime.datetime.utcnow(),
        )
        db.add(thread_meta)

    # Mark summary as used
    summary.is_used = True
    db.commit()

    return new_content


def build_content_prompt(topic,summary, key_points, config, content_type, tweet_count, article_length, include_citations, citation_count, sources, max_tweet_length=None):
    """
    Build the prompt to send to the LLM based on user style and request config.
    """
    prompt = f"""
    You are a helpful AI assistant skilled in writing social media content and making viral content.
    Generate a {content_type} based on the user's style and preferences.

    Persona: {config.get('persona')}
    Tone: {config.get('tone')}
    Style: {config.get('style')}
    Language: {config.get('language')}

    Content should be an original thought or commentary on the {topic} but making sure that it is not hallucinated or false by: 
    - referencing facts in this summary: "{summary}"
    - Include key points not as list items, but try weave them into the content if relevant, in a natural way:
    {chr(10).join(f"- {point}" for point in key_points)}
    - {'Include' if include_citations else 'Do not include'} source citations.
    - If citations are included, show up to {citation_count} most relevant ones.
    - {'Use citations at the end of each tweet or as final tweets.' if content_type == 'thread' else 'Include citations as a numbered list at the end.'}
    - Vary tweet lengths naturally (some short, some longer, max {max_tweet_length or 280} chars).
    - Make sure no tweet is beyond the maximum tweet length. very important.
    - Target: {tweet_count} tweets or {article_length} words.

    Structure the output for threads as follows:
    - Each tweet separated by this exact marker: "===="
    - Do not number tweets (no 1/6, 2/6)
    - Include max 2 relevant hashtags per tweet
    - Do not include sources or links directly — we’ll handle that elsewhere
    - Close off the thread or article naturally and invite discussion.

    
    """
    return prompt.strip()


import re

def split_into_tweets(text: str, max_parts: int = 10) -> list[str]:
    # Split on "====" surrounded by any whitespace (spaces, tabs, newlines)
    tweets = re.split(r"\s*====\s*", text.strip())

    # Limit to max tweets if needed
    tweets = tweets[:max_parts]
    total = len(tweets)

    # Add numbering like 1/6, 2/6
    numbered_tweets = [f"{i+1}/{total}  \n{tweet.strip()}" for i, tweet in enumerate(tweets)]
    return numbered_tweets

# Selects top N citations based on relevance and freshness
def select_top_citations(sources: list, max_count: int) -> list:
    """
    Returns the top sources sorted by:
    1. relevance_score (descending)
    2. freshness_score (descending)
    """
    sorted_sources = sorted(
        sources,
        key=lambda s: (
            float(s.relevance_score or 0),
            float(s.freshness_score or 0)
        ),
        reverse=True
    )
    return sorted_sources[:max_count]


def clean_split_tweets(tweets: list[str]) -> list[str]:
    """
    Cleans split tweets by trimming and removing empty entries.
    """
    return [t.strip() for t in tweets if t.strip()]

def join_tweets_for_platform(tweets: list[str], platform: str) -> str:
    """
    Joins cleaned tweets appropriately for the given platform.

    Args:
        tweets: Cleaned list of tweet strings.
        platform: 'typefully' or 'x'

    Returns:
        str: Joined tweet string ready to store or post.
    """
    if platform == "typefully":
        return "\n\n\n\n".join(tweets)

    elif platform == "x":
        # Future: Use actual threading via Twitter/X API per tweet
        # For now, join like Typefully
        return "\n\n\n\n".join(tweets)

    else:
        raise ValueError(f"Unsupported platform: {platform}")




# --- Prompt Builder ---
# def build_content_prompt(summary, key_points, config, content_type, tweet_count, article_length, include_citations, citation_count, sources, max_tweet_length=None):
#     """
#     Build the prompt to send to the LLM based on user style and request config.
#     """
#     prompt = f"""
# You are a helpful AI assistant skilled in writing social media content.
# Generate a {content_type} based on the user's style and preferences.

# Persona: {config.get('persona')}
# Tone: {config.get('tone')}
# Style: {config.get('style')}
# Language: {config.get('language')}

# Content should be:
# - Based on this summary: "{summary}"
# - Include key points:
# {chr(10).join(f"- {point}" for point in key_points)}
# - {'Include' if include_citations else 'Do not include'} source citations.
# - If citations are included, show up to {citation_count} most relevant ones.
# - {'Use citations at the end of each tweet or as final tweets.' if content_type == 'thread' else 'Include citations as a numbered list at the end.'}
# - Vary tweet lengths naturally (some short, some longer, max {max_tweet_length or 280} chars).
# - Target: {tweet_count} tweets or {article_length} words.

# Generate now:
# """
#     return prompt.strip()

# --- Tweet Splitter ---
# def split_into_tweets(text: str, max_count: int) -> list[str]:
#     """
#     Future: NLP sentence split + max_tweet_length enforcement.
#     """
#     lines = [line.strip() for line in text.split("\n") if line.strip()]
#     return lines[:max_count]