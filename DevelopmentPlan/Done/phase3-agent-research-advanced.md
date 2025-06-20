# Phase 3: Enhanced Research Agent

## Purpose
Upgrade the Research Agent to include external search via Google, advanced verification, and source reuse management for quality and efficiency.

---

## 1. Google Search Integration

### Input Additions
- Google API key
- Custom Search Engine ID

### Implementation Steps
```python
from app.services.google_search import get_google_search_results

def fetch_google_sources(topic, limit):
    return get_google_search_results(topic, limit)
```

### Result Processing
- Remove duplicates (based on URL or domain similarity)
- Combine with AI-suggested sources
- Enforce `max_sources_per_request`

### Notes
- Respect rate limits
- Fallback to AI-only if API fails

---

## 2. Advanced Source Verification

### New Checks
- **Domain Reputation**: whitelist trusted domains, blacklist spammy ones
- **HTTP Status**: confirm 200 response
- **Paywall Check**: flag inaccessible content
- **Metadata Extraction**: use BeautifulSoup for title, author, pub date

### Relevance & Freshness Scoring
```python
relevance = calculate_embedding_similarity(topic_embedding, source_embedding)
freshness = compute_freshness_score(publication_date)
```
- Store scores in `research_sources`
- Discard if relevance < `source_relevance_threshold`

---

## 3. Source Reuse Management

### Goal
Avoid using stale or overly repeated sources for new content.

### Implementation Steps
- Hash the `content_topic` → `content_topic_hash`
- Hash the source URL → `source_url_hash`
- Check against `topic_source_usage` table
- Reject sources over `source_reuse_threshold`
- Increment `usage_count` on save

### SQL Note
```sql
CREATE TABLE topic_source_usage (
    id SERIAL PRIMARY KEY,
    content_topic_hash VARCHAR(64),
    source_url_hash VARCHAR(64),
    usage_count INTEGER DEFAULT 1,
    last_used_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(content_topic_hash, source_url_hash)
);
```

---

## Completion Criteria
- [x] Google Search results integrated and deduplicated
- [x] Verified sources meet relevance and freshness criteria
- [x] Reuse logic enforces diversity and tracks source frequency

## Notes
- Still fallback gracefully if fewer than `min_sources_required`
- Add retry logic on Google failures
- Maintain modularity for easier testing

---

> **Next: Content Generation Agent — build content from these refined sources.**
