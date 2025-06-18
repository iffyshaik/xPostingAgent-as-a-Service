# Configuration & Environment Variables

## Environment File: `.env`
```dotenv
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ai_platform

# Redis (Queue)
REDIS_URL=redis://localhost:6379

# Secret Key
SECRET_KEY=your-secret-key

# AI Providers
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
DEFAULT_AI_PROVIDER=openai

# Google Search API
GOOGLE_SEARCH_API_KEY=your-google-search-key
GOOGLE_SEARCH_ENGINE_ID=your-search-engine-id

# Typefully API
TYPEFULLY_API_KEY=your-typefully-key

# X (Twitter) API
X_API_KEY=your-x-api-key
X_API_SECRET=your-x-api-secret
```

## Configuration Patterns
Use a central `config.py` file:
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    secret_key: str
    openai_api_key: str
    anthropic_api_key: str
    google_search_api_key: str
    google_search_engine_id: str
    typefully_api_key: str
    x_api_key: str
    x_api_secret: str
    default_ai_provider: str = "openai"

    class Config:
        env_file = ".env"

settings = Settings()
```

## Runtime Switching
```python
if settings.default_ai_provider == "openai":
    use_openai()
else:
    use_anthropic()
```

## Notes
- Validate all required settings on app startup
- Keep `.env.example` (no real keys) in Git
- Use `.env.staging` / `.env.prod` for multi-environment deployment
- Store secrets in vaults (e.g., AWS Secrets Manager) in production

---

> **This config setup allows secure, flexible, and environment-portable deployments.**
