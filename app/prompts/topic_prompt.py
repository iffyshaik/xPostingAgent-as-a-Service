# app/prompts/topic_prompt.py

"""
This file defines the prompt template for the Topic Generation Agent.
The template takes user configurations and original topic and generates a refined content topic using LLM.
"""

from jinja2 import Template

def build_topic_prompt(original_topic: str, user_config: dict, content_type: str) -> str:
    """
    Build a refined content topic prompt based on user configuration and input topic.
    """
    template_str = """
You are an expert content strategist. Transform the following topic into an engaging, specific angle that would make for compelling {{ content_type }} content.

User's writing style: {{ persona }}
Tone preference: {{ tone }}
Content style: {{ style }}

Original topic: {{ original_topic }}

Generate a specific, engaging angle or question that:
1. Is more focused than the original topic
2. Would naturally lead to {{ tweet_count }} tweets OR {{ article_length }} words
3. Matches the user's preferred tone and style
4. Would encourage engagement and discussion

Respond with only the refined content topic, no explanation.
    """

    system_defaults = {
        "tweet_count": 10,
        "article_length": 1000
    }

    rendered_prompt = Template(template_str).render(
        content_type=content_type,
        persona=user_config.get("persona", "Professional"),
        tone=user_config.get("tone", "informative"),
        style=user_config.get("style", "conversational"),
        original_topic=original_topic,
        **system_defaults
    )

    return rendered_prompt.strip()
