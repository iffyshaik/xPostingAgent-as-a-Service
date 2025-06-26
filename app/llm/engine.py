# app/llm/engine.py

"""
Handles communication with the configured LLM provider (OpenAI or Anthropic).
Supports per-agent model overrides. Defaults fall back to OPENAI_MODEL from .env.
"""

import openai
from app.config import settings

# Set provider (only OpenAI supported for now)
DEFAULT_PROVIDER = settings.default_ai_provider

# Agent-specific model mapping
DEFAULT_MODELS = {
    "topic_agent": settings.openai_model_topic_agent or "gpt-4",
    "summary_agent": settings.openai_model_summary_agent or "gpt-4-turbo",
    "content_agent": settings.openai_model_content_agent or "gpt-4-turbo",
    "research_agent":settings.openai_model_research_agent or "gpt-4-turbo",
}

def generate_completion(prompt: str, model_name: str = None, agent: str = "default") -> str:
    """
    Sends a prompt to the configured LLM and returns the generated response.

    Args:
        prompt (str): Prompt text to send.
        model_name (str, optional): Override model name directly.
        agent (str, optional): Agent name ('topic_agent', etc.) for default model lookup.

    Returns:
        str: Generated response from the LLM.
    """
    if DEFAULT_PROVIDER != "openai":
        raise NotImplementedError("Only OpenAI is supported at the moment.")

    selected_model = model_name or DEFAULT_MODELS.get(agent, settings.openai_model)
    print(f"🤖 Using model for {agent}: {selected_model}")

    response = openai.chat.completions.create(
        model=selected_model,
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )

    return response.choices[0].message.content.strip()
