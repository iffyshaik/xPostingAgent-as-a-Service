"""
Embedding Similarity
--------------------
Uses OpenAI's embedding API to score similarity between content topic and source text.
"""

import openai
import numpy as np
from typing import List
from app.config import settings
from openai import OpenAI

openai.api_key = settings.openai_api_key

client = OpenAI(api_key=settings.openai_api_key)


def get_embedding(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    """
    Gets an embedding vector using the OpenAI client (>=1.0.0).
    """
    try:
        response = client.embeddings.create(
            input=[text],
            model=model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"❌ Failed to get embedding: {e}")
        return []

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculates cosine similarity between two vectors.
    Returns a float between 0.0 and 1.0
    """
    try:
        a = np.array(vec1)
        b = np.array(vec2)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    except Exception as e:
        print(f"❌ Cosine similarity failed: {e}")
        return 0.0

def calculate_embedding_similarity(text1: str, text2: str) -> float:
    """
    Computes embedding-based similarity between two pieces of text.
    """
    vec1 = get_embedding(text1)
    vec2 = get_embedding(text2)
    if not vec1 or not vec2:
        return 0.0
    return cosine_similarity(vec1, vec2)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()  # Load API key from .env

    topic = "Impact of AI on education systems"
    article = (
        "Artificial Intelligence is being used to personalise learning for students by "
        "adapting content to their pace and needs. It enables tailored teaching strategies."
    )

    score = calculate_embedding_similarity(topic, article)
    print(f"🧠 Embedding Similarity Score: {score:.4f}")
