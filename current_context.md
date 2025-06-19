# Project Context Handoff

## What We're Building

A multi-tenant SaaS platform that uses AI to generate social media threads and articles from user-submitted topics. It performs research, summarisation, and content creation, and can publish to X (Twitter) or Typefully.

---

## Current Phase

**Phase 2: Topic Generation Agent** ✅ COMPLETE

---

## Tech Stack

* Python 3.11+ / FastAPI
* PostgreSQL + SQLAlchemy ORM
* Alembic for migrations
* Celery + Redis for async tasks
* OpenAI / Anthropic API support
* Docker for local and cloud deployment

---

## AI Model Configuration Strategy

We are currently supporting model overrides on a **per-agent basis**, with fallback to a global default. This is configured in `config.py` and used in the `llm.engine` module. Each agent can either:

* Use the `model_name` passed at runtime
* Fall back to its agent-specific model from environment variables
* Ultimately default to `openai_model`

### `.env` Configuration Example:

```dotenv
OPENAI_MODEL=gpt-4
OPENAI_MODEL_TOPIC_AGENT=gpt-4
OPENAI_MODEL_SUMMARY_AGENT=gpt-4-turbo
OPENAI_MODEL_CONTENT_AGENT=gpt-4-turbo
```

### In `config.py`:

```python
class Settings(BaseSettings):
    ...
    openai_model: str = "gpt-4"
    openai_model_topic_agent: str = "gpt-4"
    openai_model_summary_agent: str = "gpt-4-turbo"
    openai_model_content_agent: str = "gpt-4-turbo"
```

---

## File/Folder Structure

```
project_root/
├── alembic/
│   ├── versions/
│   └── env.py
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI entrypoint
│   ├── config.py                    # Loads settings from .env
│   ├── database.py                  # DB engine, session factory
│   ├── api/
│   │   └── auth.py                  # Auth routes
│   ├── schemas/
│   │   └── auth_schemas.py          # Pydantic models for register/login
│   ├── services/
│   │   └── auth_service.py          # Auth logic (hashing, JWT, current user)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── user_configurations.py
│   │   ├── system_configurations.py
│   │   ├── requests.py
│   │   └── user_sessions.py
│   ├── agents/
│   │   └── topic_agent.py           # Topic generation logic using LLM
│   ├── prompts/
│   │   └── topic_prompt.py          # Jinja2 template for topic prompt
│   └── llm/
│       ├── __init__.py
│       └── engine.py                # Handles LLM calls with per-agent model config
├── tests/
│   └── test_topic_agent.py          # Pytest for topic agent flow
├── .env
├── pytest.ini
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Defined Classes and Functions

### `app/config.py`

* `Settings(BaseSettings)`: Loads all environment variables
* `settings`: Global instance of `Settings`

### `app/database.py`

* `engine`: SQLAlchemy engine from `DATABASE_URL`
* `SessionLocal`: Session factory
* `Base`: Declarative base

### `app/main.py`

* `app`: FastAPI instance
* Includes routes from `auth.py`

### `app/api/auth.py`

* `register(payload: UserRegister)`: Registers a user (placeholder logic)
* `login(payload: UserLogin)`: Logs in a user, returns JWT

### `app/schemas/auth_schemas.py`

* `UserRegister`: Validates email + password for register
* `UserLogin`: Validates email + password for login

### `app/services/auth_service.py`

* `hash_password(password)`: Hashes password using bcrypt
* `verify_password(password, hashed)`: Verifies hashed password
* `create_token(user_id)`: Issues JWT token
* `get_current_user(token)`: Validates JWT and returns `user_id`
* `register_user(payload)`: Placeholder — just returns hash for now
* `login_user(payload)`: Issues token, stores hashed token in DB

### `app/models/user_sessions.py`

* `UserSession`: SQLAlchemy model for storing user\_id, token\_hash, expiry, created\_at

### `app/prompts/topic_prompt.py`

* `build_topic_prompt(original_topic, user_config, content_type)`: Builds a prompt string using Jinja2 template with placeholders like persona, tone, and style.

### `app/agents/topic_agent.py`

* `generate_content_topic(request_id, original_topic, user_config, content_type, user_id)`:

  * Builds prompt using `build_topic_prompt`
  * Sends prompt to OpenAI via `generate_completion`
  * Updates the `requests` table in DB with `content_topic` and sets status to `researching`
  * Handles error logging and fallback

### `app/llm/engine.py`

* `generate_completion(prompt, model_name=None, agent="default")`: Sends a prompt to OpenAI GPT, supports:

  * Agent-specific default models via config
  * Runtime model override

---

## Tests

### `tests/test_topic_agent.py`

* Uses `pytest` with `unittest.mock.patch` to stub OpenAI call
* Creates dummy `User` and `Request`
* Tests:

  * That the agent generates a refined topic
  * That the `requests` table is updated correctly

---

## What’s Next

🔜 In the next session, we will:

1. Start the **Research Agent** to retrieve high-quality sources
2. Use the `content_topic` field we just generated
3. Fetch and validate web + AI-suggested sources
4. Store them in the `research_sources` table

---

*Last updated: 2025-06-19 09:47:00*
