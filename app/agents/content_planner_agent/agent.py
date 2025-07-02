"""
agent.py - Main logic for the Content Planner Agent.

This agent:
1. Receives a topic and user preferences (persona, tone, style, content_type)
2. Loads a planning prompt from the local `prompts/` folder
3. Fills in the user data to format the prompt
4. Sends it to the configured LLM and parses the JSON response
5. Returns a validated ContentPlannerOutput object

This agent expects `get_llm()` from `llm_config.py` and schemas from `schema.py`.
"""

import json
import re
from pathlib import Path
from pydantic import ValidationError
from app.agents.content_planner_agent.schema import ContentPlannerInput, ContentPlannerOutput
from app.agents.content_planner_agent.llm_config import get_llm
from app.utils.prompts import load_prompt

class ContentPlannerAgent:
    def __init__(self, llm=None):
        self.llm = llm or get_llm()
        self.prompt_template_path = Path(__file__).parent / "prompts" / "planner_prompt.txt"

    def run(self, input_data: ContentPlannerInput) -> ContentPlannerOutput:
        prompt_template = load_prompt(self.prompt_template_path)
        filled_prompt = prompt_template.format(
            original_topic=input_data.original_topic,
            persona=input_data.persona,
            tone=input_data.tone,
            style=input_data.style,
            content_type=input_data.content_type,
        )

        response = self.llm.generate(prompt=filled_prompt)
        raw_output = response.content

        # 🔍 Print raw output for debugging
        #print("🧾 Raw LLM Output:", repr(raw_output))

        # Proceed to parse...
        try:
            cleaned = raw_output.strip("`\n ")
            cleaned = re.sub(r"^```(json)?", "", cleaned, flags=re.IGNORECASE).strip()
            cleaned = re.sub(r"```$", "", cleaned).strip()
            if not cleaned.startswith("{") and '"framed_topic"' in cleaned:
                cleaned = "{" + cleaned
            if not cleaned.endswith("}"):
                cleaned = cleaned + "}"

            print("\n🧽 Cleaned JSON for parsing:")
            print(cleaned)

            parsed = json.loads(cleaned)
        except Exception as e:
            raise RuntimeError(f"Could not parse LLM response: {e}")

        try:
            return ContentPlannerOutput(**parsed)
        except ValidationError as e:
            raise RuntimeError(f"Parsed JSON is invalid: {e}")




