# Phase 4: Content Generation Agent

## Purpose
Convert the combined summary and key points into a publishable thread or article tailored to user preferences.

## Input Schema
```json
{
  "combined_summary": "string",
  "combined_key_points": ["string", "string", ...],
  "user_configurations": {
    "persona": "string",
    "tone": "string",
    "style": "string",
    "language": "string"
  },
  "content_type": "thread" | "article",
  "tweet_count": 10,  // for threads
  "article_length": 1000,  // for articles (words)
  "include_source_citations": true | false
}
```

## Output
- `generated_content` (text)
- `thread_structure` (if thread)
- Stored in `content_queue` table with draft status

## Implementation Steps

### Step 1: Plan Content Structure
- For threads: determine tweet breakdown from key points
- For articles: outline with sections, transitions, conclusion

### Step 2: Generate Content via LLM
```python
from app.llm.engine import generate_completion

def create_content(summary, key_points, user_config, content_type):
    prompt = build_content_prompt(summary, key_points, user_config, content_type)
    return generate_completion(prompt)
```

### Prompt Template Notes
- Use persona/tone/style/language inputs
- Respect tweet/word count limits
- Include citations if requested

### Step 3: Format and Validate Output
- For threads:
  - Ensure each tweet ≤ 280 characters
  - Split long tweets if needed
  - Add optional citation tweets

- For articles:
  - Check word count
  - Verify readability and coherence

### Step 4: Store in `content_queue`
- Fields:
  - `generated_content`
  - `status = 'draft'`
  - `content_type`
  - `platform`
  - `scheduled_for = null`
  - `created_at`

## Completion Criteria
- [x] Content matches user’s tone, persona, and style
- [x] Valid structure for content_type
- [x] Stored and ready for approval/publishing

## Notes
- Set up `thread_metadata` if thread content
- Keep citation logic optional and platform-specific
- Perform basic offensive content checks before saving

---

> **Next: Implement content queue approval and publishing workflow.**
