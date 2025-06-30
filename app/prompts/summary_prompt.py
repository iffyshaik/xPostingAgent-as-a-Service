"""
Prompt builder for the Summary Agent.
Takes combined source summaries and key points and builds a prompt for the LLM.
"""

def build_summary_prompt(text: str, key_points: list[str], length_limit: int, content_type: str) -> str:
    """
    Builds the system prompt to generate a clean summary and distinct key points.

    Args:
        text (str): Combined summaries from sources.
        key_points (list): Merged key points from each source.
        length_limit (int): Target word count for the summary.
        content_type (str): 'thread' or 'article'

    Returns:
        str: Final prompt to send to the LLM.
    """
    return f"""
You are a summarisation expert. Given the following research inputs, create a coherent summary and extract {len(key_points)} distinct key points.

Summaries:
{text}

Make the result suitable for a content creator preparing a {content_type}. 
Target length: {length_limit} words.

Output the final result in the following format:
Summary:
[Your summary here]

Key Points:
1. ...
2. ...
"""



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
