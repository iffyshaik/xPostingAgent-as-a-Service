# Phase 5: Platform Integration

## Purpose
Enable publishing of content to external platforms, starting with Typefully and X (Twitter).

---

## Supported Platforms
- **Typefully**: queue and schedule posts via API
- **X (Twitter)**: direct publishing using user auth

## Platform Field in `requests` and `content_queue`
- Values: `typefully`, `x`
- Used to route publishing logic appropriately

---

## Typefully Integration

### API Requirements
- API key from Typefully
- Endpoint: `POST https://api.typefully.com/v1/drafts`

### Payload Example
```json
{
  "content": "Full thread content here",
  "platform": "twitter",
  "scheduleTime": "2024-01-01T10:00:00Z"
}
```

### Response Handling
- On success: store `post_response`
- On failure: log `error_message`, retry if applicable

### Notes
- No OAuth needed; platform-wide API key is sufficient
- Rate-limited to ~50 requests/minute (check docs)

---

## X (Twitter) API Integration

### OAuth 2.0 Flow (User Context)
- Requires `x_api_key`, `x_api_secret`
- Use access token obtained during user onboarding

### Posting Endpoint
```http
POST https://api.twitter.com/2/tweets
```
Payload for single tweet:
```json
{
  "text": "Tweet content"
}
```
- For threads: loop through with reply chaining (use `in_reply_to_tweet_id`)

### Rate Limits
- 300 tweets / 3 hours per user (standard)
- Use exponential backoff for retries

---

## Completion Criteria
- [x] Platform field routes logic correctly
- [x] Typefully posting returns confirmation
- [x] Twitter threads are chained correctly
- [x] Errors are captured and retries logged

## Notes
- Support dry-run mode in dev
- Add `platform_posted_id` field for auditing
- Eventually support LinkedIn, Substack, Bluesky

---

> **Next: Build the user-facing UI for configuration and content review.**