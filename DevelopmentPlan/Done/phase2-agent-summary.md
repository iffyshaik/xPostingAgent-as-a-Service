# Phase 2: Basic Pipeline - Summary Agent

## Purpose
Synthesize verified research sources into a coherent summary and extract key points for downstream content generation.

## Input Schema
```json
{
  "request_id": "int",
  "verified_sources": [
    {
      "url": "string",
      "title": "string",
      "summary": "string",
      "key_points": ["string", "string", ...]
    },
    ...
  ],
  "target_length": 1000,  // in words
  "content_type": "thread" | "article"
}
```

## Output
- `combined_summary` (text)
- `combined_key_points` (array)
- Stored in `summaries` table with `request_id`, `user_id`

## Implementation Steps

### Step 1: Combine and Clean Source Summaries
```python
def combine_summaries(sources):
    all_text = "\n\n".join([src["summary"] for src in sources])
    return all_text
```

### Step 2: Prompt the LLM
```python
from app.llm.engine import generate_completion

def generate_summary(text, key_points, length_limit):
    prompt = f"""
You are a summarisation expert. Given the following research inputs, create a coherent summary and extract {len(key_points)} key points.

Summaries:
{text}

Make the result suitable for a content creator preparing a {length_limit}-word piece. Output a short summary and key points.
"""
    return generate_completion(prompt)
```

### Step 3: Parse and Store Output
- Split the LLM output into `combined_summary` and `combined_key_points`
- Save to the `summaries` table

## Testing Requirements
- Handles duplicate/overlapping key points
- Produces concise, non-redundant summaries
- Handles content edge cases (e.g. contradictory sources)

## Completion Criteria
- [x] Summary fits within word limit
- [x] Key points are distinct and actionable
- [x] Data is saved in `summaries` table with linkage
- [x] Robust fallback if one source is missing key fields

## Notes
- Set `is_used = True` when the summary is used for content generation
- Can add source attribution in a future phase

---

> **Next: Build the Content Generation Agent to convert summaries into threads or articles.**
