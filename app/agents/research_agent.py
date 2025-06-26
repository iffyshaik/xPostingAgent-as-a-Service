#app/agents/research_agents.py

"""
Research Agent
--------------
Fetches high-quality sources for a given topic using AI + Google,
verifies each one, scores for relevance, and stores the best into the database.
"""

from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app.database import SessionLocal
from app.models.research_sources import ResearchSource

# Modular services
from app.services.google_search import get_google_search_results
from app.services.ai_source_discovery import discover_sources_with_ai
from app.services.source_verification import (
    is_url_accessible,
    extract_page_metadata,
    check_relevance_with_ai,
)
from app.services.embedding_similarity import calculate_embedding_similarity
from app.services.source_reuse import is_source_overused, increment_source_usage

from app.llm.engine import generate_completion
from app.prompts.summary_prompt import build_source_summary_prompt
from app.agents.summary_agent import parse_llm_output


def generate_research_sources(
    request_id: int,
    content_topic: str,
    user_id: int,
    limit: int = 5,
    preference: str = "balanced"
) -> bool:
    """
    Runs the full research pipeline:
    1. Discovers sources via AI and Google
    2. Deduplicates by URL
    3. Verifies each source (accessibility, relevance, reuse)
    4. Scores relevance via embeddings
    5. Stores valid sources to research_sources table

    Args:
        request_id (int): ID of the content request
        content_topic (str): Refined topic to research
        user_id (int): Owner of the request
        limit (int): Max number of sources to save
        preference (str): Source style (balanced, science_heavy, general)

    Returns:
        bool: True if any valid sources stored
    """
    db = SessionLocal()
    try:
        print(f"\n🔍 Starting research for topic: {content_topic}")

        # --- 1. Discover sources from AI and Google ---
        ai_sources = discover_sources_with_ai(content_topic, limit, preference)
        google_sources = get_google_search_results(content_topic, limit)
        all_sources = ai_sources + google_sources

        print(f"\n📦 Total discovered: {len(all_sources)} sources")

        # --- 2. Deduplicate by URL ---
        seen_urls = set()
        deduped_sources = []
        for src in all_sources:
            url = src.get("url") or src.get("source_url")
            if url and url not in seen_urls:
                src["url"] = url  # standardise
                deduped_sources.append(src)
                seen_urls.add(url)

        print(f"🔁 Deduplicated to {len(deduped_sources)} unique URLs")

        verified = 0
        for source in deduped_sources:
            url = source["url"]

            # --- Skip if already in DB for this request ---
            existing = db.query(ResearchSource).filter_by(request_id=request_id, url=url).first()
            if existing:
                print(f"🗃️ Already stored: {url}")
                continue

            # --- Skip if overused for this user+topic ---
            if is_source_overused(user_id, content_topic, url):
                print(f"🚫 Overused for topic: {url}")
                continue

            # --- Check accessibility ---
            accessible, status = is_url_accessible(url)
            if not accessible:
                print(f"❌ URL not accessible: {url} | Reason: {status}")
                # Log it in DB anyway for analysis
                db_source = ResearchSource(
                    request_id=request_id,
                    user_id=user_id,
                    source_type=source.get("source", "unknown"),
                    url=url,
                    title=source.get("title", "N/A"),
                    author=source.get("authors", "N/A"),
                    verification_status="failed",
                    access_status=status,
                    verification_attempts=1,
                    last_verified_at=datetime.utcnow()
                )
                db.add(db_source)
                db.commit()
                continue

            # --- Extract metadata from page ---
            meta = extract_page_metadata(url)
            if not meta or "snippet" not in meta:
                print(f"⚠️ Skipping: Metadata missing for {url}")
                continue

            snippet = meta["snippet"]

            # --- Use LLM for a quick relevance judgement ---
            relevance_summary = check_relevance_with_ai(snippet, content_topic)

            # --- Use embeddings for numerical similarity ---
            relevance_score = calculate_embedding_similarity(content_topic, snippet)
            print(f"🧠 Relevance = {relevance_score:.2f} | {relevance_summary[:80]}...")

            if relevance_score < 0.7:
                print(f"⚠️ Too weak relevance: {url}")
                continue

            # Summarise the snippet/title and store result
            summary_prompt = build_source_summary_prompt(snippet or meta.get("title") or url)
            llm_response = generate_completion(summary_prompt, agent="source_summariser")
            summary, key_points = parse_llm_output(llm_response)

            db_source.summary = summary
            db_source.key_points = key_points


            # --- Store to DB ---
            db_source = ResearchSource(
                request_id=request_id,
                user_id=user_id,
                source_type=source.get("source", "unknown"),
                url=url,
                title=meta.get("title") or source.get("title"),
                author=source.get("authors", "N/A"),
                publication_date=None,
                verification_status="verified",
                relevance_score=relevance_score,
                freshness_score=0.5,  # ⏳: placeholder
                summary=summary,
                key_points=key_points,
                is_used=False,
                verification_attempts=1,
                last_verified_at=datetime.utcnow()
            )
            db.add(db_source)
            increment_source_usage(user_id, content_topic, url)
            verified += 1

            if verified >= limit:
                break

        db.commit()

        if verified > 0:
            print(f"\n✅ Stored {verified} verified sources.")
            return True
        else:
            print(f"\n⚠️ No high-quality sources stored.")
            return False

    except SQLAlchemyError as e:
        db.rollback()
        print(f"\n🔥 SQLAlchemy Error: {e}")
        return False
    except Exception as e:
        print(f"\n🔥 Unhandled Error: {e}")
        return False
    finally:
        db.close()
