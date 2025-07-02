"""
prompts.py - Utility functions for loading prompt templates from file.

Used by agents to load and format their LLM prompt files (e.g., .txt files with {variables}).

This keeps file I/O clean and reusable across all agents.
"""

from pathlib import Path

def load_prompt(path: Path) -> str:
    """
    Reads a prompt file from disk and returns its string contents.

    Args:
        path (Path): Path to the prompt file

    Returns:
        str: Prompt content as a string
    """
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")

    return path.read_text(encoding="utf-8").strip()
