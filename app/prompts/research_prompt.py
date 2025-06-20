# research_prompt.py
# Builds an AI prompt to fetch sources based on content topic and preference

def build_research_prompt(topic: str, preference: str, max_sources: int) -> str:
    return f"""
You are a research assistant. Find {preference} sources (but you can still include URLs, articles, or papers) related to the following topic:

"{topic}"

Respond with a list in this format:
1. [Title] by [Author] - [URL]
2. ...
Only include accessible, high-quality sources.

Please limit to no more than {max_sources} sources.

"""
