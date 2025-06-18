# Phase 4: Content Queue & Validation

## Purpose
Manage the lifecycle of generated content through approval, scheduling, posting, and validation workflows.

## Tables Involved
- `content_queue`
- `thread_metadata`

## Content Status Flow
```
draft → approved → scheduled → posted
                     ↘ failed
```

---

## Draft Storage (Initial Insertion)
Fields:
- `request_id`, `user_id`
- `generated_content`
- `content_type`: `thread` or `article`
- `status = 'draft'`
- `platform`: `x`, `typefully`, etc.
- `created_at`

## Approval API
```http
PUT /content/queue/{content_id}/approve
```
- Validates structure
- Flags suspicious/offensive content (basic checks)
- Sets status to `approved`

## Scheduling API
```http
PUT /content/queue/{content_id}/schedule
Body: { "scheduled_for": "2024-01-01T10:00:00Z" }
```
- Sets `status = scheduled`
- Validates date format and platform compatibility

## Posting API
```http
POST /content/queue/{content_id}/post
```
- Calls the publishing service for the relevant platform
- On success:
  - `status = posted`
  - `posted_at = now()`
  - Save `post_response`
- On failure:
  - `status = failed`
  - Save `error_message`

---

## Thread Metadata Storage
Table: `thread_metadata`
- `content_queue_id`
- `requested_tweet_count`, `actual_tweet_count`
- `max_tweet_length` (default 280)
- `thread_structure`: JSON array of tweets
- Optional: `citation_tweets`

---

## Completion Criteria
- [x] Draft content correctly queued
- [x] Approval and validation checks in place
- [x] Scheduling logic respects platform constraints
- [x] Posting logic handles success and failure cleanly
- [x] Threads tracked with metadata

## Notes
- Use structured logging for post attempts
- Use Celery worker for async scheduled posting
- Extend later with analytics or reposting logic

---

> **Next: Add integration with Typefully and X for actual publishing.**
