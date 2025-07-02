"""
llm_clients.py - Shared LLM wrapper classes for all agents.

Each client class (e.g. OpenAIClient, AnthropicClient) provides a standard `.generate(...)` method
so agents can switch providers easily.

Supports both single prompt and chat-style messages.
"""

import openai
from typing import Optional, List, Union
from pydantic import BaseModel
from app.config import settings

class LLMResponse(BaseModel):
    content: str
    raw: dict

class OpenAIClient:
    def __init__(self, model="gpt-4", temperature=0.7, max_tokens=1000, system_prompt=None):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_prompt = system_prompt
        self.client = openai.OpenAI(api_key=settings.openai_api_key)

    def generate(self, prompt=None, messages=None) -> LLMResponse:
        if messages is None:
            if prompt is None:
                raise ValueError("Provide prompt or messages")
            messages = []
            if self.system_prompt:
                messages.append({"role": "system", "content": self.system_prompt})
            messages.append({"role": "user", "content": prompt})
            
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
    


        content = response.choices[0].message.content.strip()
        return LLMResponse(content=content, raw=response.model_dump())


class FakeLLM:
    def __init__(self, predefined_output: Union[str, dict] = None):
        self.predefined_output = predefined_output or '{"framed_topic": "Test", "content_angle": "commentary", "structure_plan": [{"title": "Test", "description": "Test section", "suggested_support": "quote"}]}'

    def generate(self, prompt=None, messages=None):
        content = (
            self.predefined_output if isinstance(self.predefined_output, str)
            else self.predefined_output.get("content", "")
        )
        return LLMResponse(content=content, raw={"fake": True})


