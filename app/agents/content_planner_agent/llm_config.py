"""
llm_config.py - Per-agent configuration for the LLM engine used by the Content Planner Agent.

This file defines which model and provider this agent should use, and how to initialise it.
It allows every agent to specify its own LLM configuration (e.g. OpenAI vs Anthropic),
including temperature, model version, max tokens, and any system prompt.

Shared LLM client classes (e.g. OpenAIClient, AnthropicClient) are expected to live in:
    app/utils/llm_clients.py

This modular design allows easy testing, swapping models, and isolated debugging per agent.
"""

from app.utils.llm_clients import OpenAIClient  # or AnthropicClient, etc.

def get_llm():
    """
    Returns a configured LLM client instance for the planner agent.
    You can change the provider or model without affecting other agents.
    """
    return OpenAIClient(
        model="gpt-4",
        temperature=0.7,
        max_tokens=1000,
        system_prompt="You are a strategic content planner. Your goal is to structure insightful, engaging content from vague user topics."
    )
