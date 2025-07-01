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