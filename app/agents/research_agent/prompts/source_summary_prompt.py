def build_source_summary_prompt(source_text: str, max_words: int = 200) -> str:
    """
    Builds a prompt to summarise a single research source and extract 3-5 key points.

    Args:
        source_text (str): The text to summarise (e.g., title, snippet, or excerpt).
        max_words (int): Target length for summary.

    Returns:
        str: Prompt formatted for LLM to summarise one source.
    """
    return f"""
You are a concise summariser for research content.

Summarise the following article snippet or source text into a clear short paragraph,
and extract 3 to 5 key points that reflect its core ideas.

Keep the summary under {max_words} words.

Text to summarise:
{source_text}

Respond in this exact format:
Summary:
[Your summary]

Key Points:
- ...
- ...
"""
