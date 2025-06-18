# Phase 6: Security Hardening & Performance Optimisation

## Purpose
Ensure the platform is production-ready by implementing robust security controls, scalability enhancements, and monitoring systems.

---

## Security Hardening

### 1. Authentication
- Use strong JWT secrets stored in env vars
- Expiry tokens within 24 hours (refresh token flow optional)
- Hash tokens in `user_sessions`

### 2. Input Validation
- Use Pydantic schemas to validate all incoming API payloads
- Reject unexpected fields
- Enforce type and value constraints

### 3. Rate Limiting
- Per-user and per-IP throttling (e.g. 100 requests/hour)
- Use Redis with middleware (e.g. `slowapi`, `fastapi-limiter`)

### 4. Access Control
- Role-based auth for admin endpoints
- Content filtering per `user_id`

### 5. Secrets Management
- All keys in `.env` file or secret manager (e.g. AWS Secrets Manager)
- Never commit secrets to Git

---

## Performance Optimisation

### 1. Caching
- Cache expensive LLM responses by prompt hash
- Optionally cache AI-generated sources with expiry

### 2. Async Task Queue
- Use Celery + Redis for all:
  - LLM calls
  - Google search
  - Content posting
- Retry failed tasks with exponential backoff

### 3. DB Indexing
- Add indexes to:
  - `user_id`
  - `request_id`
  - `created_at`
  - `status`

### 4. Content Pipeline Timeout Handling
- Set timeouts on:
  - LLM requests (60s max)
  - External APIs (5s max)
- Use `asyncio` + `httpx` for non-blocking requests

---

## Monitoring & Logging

### Structured Logs
- Log request_id, user_id, stage, error, and timestamp
- Use log levels: `info`, `warning`, `error`

### Error Alerts
- Track:
  - LLM failures
  - High response latency
  - Daily quota breaches
- Send alerts via email/Slack/Webhooks

### Performance Metrics
- Time per pipeline stage (e.g. research, summary)
- Number of retries
- Queue task age

---

## Completion Criteria
- [x] Rate limiting and auth validated in staging
- [x] LLM and API timeouts in place
- [x] Async processing tested under load
- [x] Monitoring tools integrated

## Notes
- Prepare load testing suite for staging
- Optional: Add circuit breaker pattern for failing APIs

---

> **This concludes the core development specification. Remaining tasks: deployment, context tracker, and documentation split.**