# AI Content Platform - Core Architecture

## Tech Stack
- **Backend**: Python 3.11+ with FastAPI
- **Database**: PostgreSQL 15+ with SQLAlchemy ORM
- **Queue System**: Celery with Redis
- **Authentication**: JWT tokens
- **AI Providers**: OpenAI, Anthropic (configurable)
- **External APIs**: Google Search API, web scraping for source verification
- **Deployment**: Docker containers
- **Development Environment**: VSCode with Python extensions

## System Flow
1. User submits a topic
2. Topic Generation Agent refines it
3. Research Agent finds relevant sources
4. Summary Agent synthesises those sources
5. Content Generation Agent creates thread/article
6. Publishing Service posts to X/Typefully or queues it

## Core Components
1. **API Gateway** - FastAPI app managing all HTTP requests
2. **Authentication Service** - Handles user login and JWT-based auth
3. **Topic Generation Agent** - Converts user topics into focused content topics
4. **Research Agent** - Gathers and verifies relevant sources
5. **Summary Agent** - Synthesises sources into summaries and key points
6. **Content Generation Agent** - Produces the final content
7. **Publishing Service** - Posts or queues for publishing
8. **Queue Manager** - Celery workers for asynchronous task handling

## Core Database Tables
- `users`
- `requests`
- `user_configurations`
- `system_configurations`

## Error Handling Pattern
- Graceful degradation if an agent fails
- Notify the user about partial results or retries
- Continue to next stage if minimum viable output is available

## Best Practice Notes
- Keep each agent modular and independently testable
- Log inputs/outputs at each stage for debugging
- Use retries and fallbacks for API failures
- Always isolate user data by `user_id`
- AI providers should be configurable per environment

---

> **Include this document in every session unless otherwise stated. It defines the foundational system assumptions.**
