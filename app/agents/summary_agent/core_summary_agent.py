"""
Summary Agent (Phase 2)
Combines verified source summaries and key points, generates a clean summary,
and stores results in the `summaries` table.
"""

from app.llm.engine import generate_completion
from app.prompts.summary_prompt import build_summary_prompt
from app.database import SessionLocal
from app.models.research_sources import ResearchSource
from app.models.requests import Request
from app.models.summaries import Summary
from sqlalchemy.orm import Session

def combine_summaries(sources: list[dict]) -> str:
    """
    Combines all source summaries into one text block.

    Args:
        sources (list): List of research source dicts.

    Returns:
        str: Combined summaries as a single string.
    """
    return "\n\n".join([src["summary"] for src in sources if src.get("summary")])


def merge_key_points(sources: list[dict]) -> list[str]:
    """
    Merges all source key points, removing duplicates.

    Args:
        sources (list): List of research source dicts.

    Returns:
        list: Distinct key points.
    """
    seen = set()
    result = []
    for src in sources:
        for kp in src.get("key_points", []):
            if kp not in seen:
                result.append(kp)
                seen.add(kp)
    return result


def parse_llm_output(response_text: str) -> tuple[str, list[str]]:
    """
    Splits the LLM output into summary and list of key points.

    Args:
        response_text (str): Raw LLM response.

    Returns:
        tuple: (summary: str, key_points: list[str])
    """
    if "Key Points:" in response_text:
        summary_part, key_part = response_text.split("Key Points:", 1)
        key_lines = [line.strip("- ").strip() for line in key_part.strip().split("\n") if line.strip()]
        return summary_part.strip(), key_lines
    return response_text.strip(), []


def generate_and_store_summary(request_id: int, verified_sources: list[dict], target_length: int, content_type: str, user_id: int):
    """
    Main pipeline: combines source summaries, prompts LLM, parses and stores result.

    Args:
        request_id (int): The request this summary belongs to.
        verified_sources (list): Verified source dicts with summary/key_points.
        target_length (int): Word length for the summary.
        content_type (str): 'thread' or 'article'.
        user_id (int): The user initiating the request.
    """
    if not verified_sources:
        print(f"⚠️ No verified sources provided for request {request_id}. Skipping summary generation.")
        
        return None
    
    
    combined_summary_text = combine_summaries(verified_sources)
    combined_key_points = merge_key_points(verified_sources)
    
    if not combined_summary_text.strip():
        print(f"⚠️ Empty combined summary for request {request_id}. Skipping.")
        return None

    prompt = build_summary_prompt(combined_summary_text, combined_key_points, target_length, content_type)
    llm_output = generate_completion(prompt, agent="summary_agent")
    summary, final_key_points = parse_llm_output(llm_output)

    with SessionLocal() as session:
        summary_obj = Summary(
            request_id=request_id,
            user_id=user_id,
            combined_summary=summary,
            combined_key_points=final_key_points,
            source_count=len(verified_sources),
            is_used=False
        )
        session.add(summary_obj)
        session.commit()
        session.refresh(summary_obj)
        return summary_obj
