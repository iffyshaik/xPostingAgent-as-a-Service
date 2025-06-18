# Phase 2: Basic Pipeline - Topic Generation Agent

## Purpose
Convert a user's raw topic into a focused, engaging content angle for a social media thread or article.

## Input Schema
```json
{
  "original_topic": "string",
  "content_type": "thread" | "article",
  "user_configurations": {
    "persona": "string",
    "tone": "string",
    "style": "string"
  }
}
```

## Output
```json
{
  "content_topic": "string"
}

// Also update the corresponding request row in the DB with:
// - content_topic
// - updated status
```

## Implementation Steps

### Step 1: Build Prompt Template
```jinja2
You are an expert content strategist. Transform the following topic into an engaging, specific angle that would make for compelling {{ content_type }} content.

User's writing style: {{ persona }}
Tone preference: {{ tone }}
Content style: {{ style }}

Original topic: {{ original_topic }}

Generate a specific, engaging angle or question that:
1. Is more focused than the original topic
2. Would naturally lead to {{ tweet_count }} tweets OR {{ article_length }} words
3. Matches the user's preferred tone and style
4. Would encourage engagement and discussion

Respond with only the refined content topic, no explanation.
```

### Step 2: Agent Logic
```python
from app.llm.engine import generate_completion
from app.prompts.topic_prompt import build_topic_prompt

def generate_content_topic(original_topic, user_config, content_type):
    prompt = build_topic_prompt(original_topic, user_config, content_type)
    result = generate_completion(prompt)
    return result.strip()
```

### Step 3: DB Integration
- Retrieve request from DB using `request_id`
- Store `content_topic` and update status to `researching`
- Log the input and output for observability

## Testing Requirements
- Validate prompt outputs for different tones and personas
- Confirm DB updates are correct
- Ensure invalid/missing input is handled gracefully

## Completion Criteria
- [x] Agent accepts valid input and returns a well-formed topic
- [x] Content topic is stored in the DB
- [x] Output respects user’s style preferences
- [x] Errors are logged with context

## Notes
- Use OpenAI GPT-4 as default model (configurable)
- Token usage should be tracked per request for quota
- Include trace ID for debugging

---

> **Next: Build the Research Agent to fetch and verify relevant sources.**