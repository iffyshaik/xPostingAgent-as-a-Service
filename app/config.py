# app/config.py
# Loads environment variables using Pydantic v2 (from pydantic-settings)

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    #Database
    database_url: str
    redis_url: str = ""
    
    #Secrets and keys
    secret_key: str = ""
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    google_search_api_key: str = ""
    google_search_engine_id: str = ""
    typefully_api_key: str = ""
    x_api_key: str = ""
    x_api_secret: str = ""
    
    #AI Provider Config
    default_ai_provider: str = "openai"
    openai_model: str = "gpt-4"
    openai_model_topic_agent: str = "gpt-4"
    openai_model_summary_agent: str = "gpt-4.1"
    openai_model_content_agent: str = "gpt-4.1"
    openai_model_research_agent: str = "gpt-4.1"

    #Feature Toggles
    enable_offensive_check: bool = True  # Toggle for content profanity check


    class Config:
        env_file = ".env"
        extra ="allow"

settings = Settings()
