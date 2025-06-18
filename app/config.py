# app/config.py
# Loads environment variables using Pydantic v2 (from pydantic-settings)

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str = ""
    secret_key: str = ""
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    google_search_api_key: str = ""
    google_search_engine_id: str = ""
    typefully_api_key: str = ""
    x_api_key: str = ""
    x_api_secret: str = ""
    default_ai_provider: str = "openai"

    class Config:
        env_file = ".env"

settings = Settings()
