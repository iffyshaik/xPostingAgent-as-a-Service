"""
AI Source Discovery
-------------------
Uses the LLM to suggest relevant sources (articles, papers, etc.)
based on the refined content topic.
"""

from typing import List, Dict
from app.llm.engine import generate_completion
from app.prompts.research_prompt import build_research_prompt

def discover_sources_with_ai(content_topic: str, source_limit: int = 5, preference: str = "balanced") -> List[Dict]:
    """
    Calls LLM to suggest sources based on the content topic.

    Args:
        content_topic (str): Refined topic string
        source_limit (int): Max number of sources to ask for
        preference (str): research preference (e.g. "science_heavy", "balanced")

    Returns:
        List[Dict]: List of sources from AI with keys like title, url, etc.
    """
    prompt = build_research_prompt(content_topic, preference, max_sources=source_limit)
    print("🧠 Prompt sent to LLM for AI Discovery:\n", prompt)

    ai_response = generate_completion(prompt, agent="research_agent")
    print("📥 AI raw response:\n", ai_response)

    return parse_ai_sources(ai_response)

def parse_ai_sources(response_text: str) -> List[Dict]:
    """
    Parses LLM output into a list of structured sources.

    Handles two formats:
    A) Verbose format:
        Type: ...
        Title: ...
        Authors: ...
        URL: ...
        Date: ...
    B) Compact format:
        1. Title by Author - URL
    """
    sources = []
    current = {}

    lines = response_text.strip().splitlines()
    for line in lines:
        line = line.strip()

        if not line:
            if current:
                sources.append(current)
                current = {}
            continue

        if line.startswith("Type:"):
            current["source"] = line.split(":", 1)[1].strip()
        elif line.startswith("Title:"):
            current["title"] = line.split(":", 1)[1].strip()
        elif line.startswith("Authors:"):
            current["authors"] = line.split(":", 1)[1].strip()
        elif line.startswith("URL:"):
            current["url"] = line.split(":", 1)[1].strip()
        elif line.startswith("Date:"):
            current["date"] = line.split(":", 1)[1].strip()

        # Fallback format: 1. Title by Author - URL
        elif line[0].isdigit() and " - " in line:
            try:
                before_dash, url = line.split(" - ", 1)
                title_part = before_dash.split(".", 1)[1].strip()
                if " by " in title_part:
                    title, author = title_part.split(" by ", 1)
                else:
                    title, author = title_part, "Unknown"
                sources.append({
                    "source": "AI Discovery",
                    "title": title.strip(),
                    "authors": author.strip(),
                    "url": url.strip(),
                    "date": "N/A",
                    "verification_status": "unverified"
                })
            except Exception as e:
                print(f"⚠️ Could not parse line: {line} → {e}")
                continue

    if current:
        sources.append(current)

    print(f"✅ Parsed {len(sources)} sources from AI")
    return sources



#FOR TESTING FILE
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    topic = "Impact of AI on education systems"
    sources = discover_sources_with_ai(topic, source_limit=3)
    for s in sources:
        print(f"{s['title']} - {s['url']}")
