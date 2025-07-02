"""
Unit tests for ContentPlannerAgent using FakeLLM to simulate AI responses.

These tests:
✅ Validate correct parsing and output structure
✅ Confirm graceful failure on invalid JSON
"""

import pytest
from app.agents.content_planner_agent.agent import ContentPlannerAgent
from app.agents.content_planner_agent.schema import ContentPlannerInput, ContentPlannerOutput
from app.utils.llm_clients import FakeLLM


def test_planner_success():
    """Test that the agent correctly parses valid JSON from the FakeLLM"""

    fake_response = """
    {
      "framed_topic": "How AI Is Changing Therapy",
      "content_angle": "commentary",
      "structure_plan": [
        {
          "title": "The AI Therapy Boom",
          "description": "Explore the rise of mental health chatbots",
          "suggested_support": "quote, app stat"
        },
        {
          "title": "Ethical Concerns",
          "description": "Bias, trust, data privacy",
          "suggested_support": "expert article"
        }
      ]
    }
    """

    from app.utils.llm_clients import FakeLLM
    from app.agents.content_planner_agent.agent import ContentPlannerAgent

    agent = ContentPlannerAgent(llm=FakeLLM(fake_response))
    input_data = ContentPlannerInput(
        original_topic="AI in therapy",
        persona="Educator",
        tone="neutral",
        style="conversational",
        content_type="article"
    )

    result = agent.run(input_data)

    assert isinstance(result, ContentPlannerOutput)
    assert result.framed_topic == "How AI Is Changing Therapy"
    assert len(result.structure_plan) == 2


def test_planner_bad_json():
    """Test that the agent raises an error if JSON is malformed"""

    from app.utils.llm_clients import FakeLLM
    from app.agents.content_planner_agent.agent import ContentPlannerAgent

    broken_response = '"framed_topic": "Missing braces"'  # Not valid JSON

    agent = ContentPlannerAgent(llm=FakeLLM(broken_response))
    input_data = ContentPlannerInput(
        original_topic="Bad JSON test",
        persona="Critic",
        tone="serious",
        style="formal",
        content_type="thread"
    )

    with pytest.raises(RuntimeError):
        agent.run(input_data)

