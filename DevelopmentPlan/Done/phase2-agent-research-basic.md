# Phase 2: Basic Pipeline - Research Agent (Basic Version)

## Purpose
Find and verify high-quality sources for a given content topic using AI and store them in the database.

## Input Schema
```json
{
  "content_topic": "string",
  "source_count_limit": 5,
  "research_preference": "balanced" | "science_heavy" | "general",
  "user_id": "int"
}
```

## Output
- A list of verified sources with:
  - URL
  - Title
  - Author
  - Summary
  - Key points
  - Relevance/freshness scores
  - Stored in `research_sources` table

## Implementation Steps

### Step 1: Use AI to Suggest Sources
```python
from app.llm.engine import generate_completion
from app.prompts.research_prompt import build_research_prompt

def generate_ai_sources(topic, preference):
    prompt = build_research_prompt(topic, preference)
    return generate_completion(prompt)
```
- Parse the AI result to extract source metadata (e.g., titles, links, authors).

### Step 2: Basic URL Verification
```python
import requests

def verify_url(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False
```
- Optionally extract title with `BeautifulSoup` or metadata parser.

### Step 3: Store in Database
- Save to `research_sources` with:
  - `request_id`
  - `user_id`
  - `source_type = ai_suggested`
  - Verification status
  - Summary (optional in basic version)

### Step 4: Minimum Source Check
- If at least `min_sources_required` are verified → proceed
- Else → fail gracefully, log, and notify user

## Completion Criteria
- [x] At least 3 verified sources stored per topic
- [x] No duplicate URLs stored
- [x] Sources linked to correct `request_id` and `user_id`
- [x] Handles API failure or timeouts with retry/fallback

## Notes
- No Google Search or arXiv integration in this phase
- Relevance scoring can be stubbed or left as placeholder
- Add basic logging for failures

---

> **Next: Build the Summary Agent to combine source content into a usable summary and key points.**