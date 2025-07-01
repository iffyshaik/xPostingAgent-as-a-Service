"""
Source Verification
-------------------
Checks if a URL is accessible and relevant to the content topic.
Extracts metadata like title, description, and body.
Optionally sends page snippet to LLM to check topic relevance.
"""

import requests
from bs4 import BeautifulSoup
from app.llm.engine import generate_completion

def is_url_accessible(url: str, timeout: int = 5) -> tuple[bool, str]:
    """
    Checks if a URL is accessible (status code < 400).

    Args:
        url (str): The URL to test

    Returns:
        bool: True if accessible, False otherwise
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        if response.status_code < 400:
            return True, "OK"
        else:
            return False, f"HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"Request error: {str(e)}"
    except Exception as e:
        return False, f"Unhandled: {str(e)}"

def extract_page_metadata(url: str, max_chars: int = 2000) -> dict:
    """
    Downloads and parses the page for metadata and content snippet.

    Returns:
        dict: {
            "title": str,
            "description": str,
            "snippet": str
        }
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code >= 400:
            return {}

        soup = BeautifulSoup(response.text, "lxml")

        title = soup.title.string.strip() if soup.title else ""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = meta_desc["content"].strip() if meta_desc and "content" in meta_desc.attrs else ""
        paragraphs = " ".join([p.get_text(strip=True) for p in soup.find_all("p")])
        snippet = f"{title}. {description}. {paragraphs}".strip()[:max_chars]

        return {
            "title": title,
            "description": description,
            "snippet": snippet
        }

    except Exception as e:
        print(f"❌ Error extracting metadata from {url}: {e}")
        return {}

def check_relevance_with_ai(page_snippet: str, content_topic: str) -> str:
    """
    Asks the LLM whether the page snippet is relevant to the topic.

    Returns:
        str: Relevance summary from LLM
    """
    prompt = f"""Evaluate the relevance of the following web content to this topic: "{content_topic}".

Content:
\"\"\"
{page_snippet}
\"\"\"

Respond with a 1-2 sentence summary of relevance, or say "Not relevant" if unrelated.
"""
    try:
        result = generate_completion(prompt, agent="research_agent")
        return result.strip()
    except Exception as e:
        print(f"⚠️ LLM relevance check failed: {e}")
        return "Unknown"


#TEST THE FILE
if __name__ == "__main__":
    test_url = "https://www.sciencedaily.com/releases/2025/06/250619090853.htm"
    topic = "Impact of AI on education systems"

    if is_url_accessible(test_url):
        print("✅ URL is accessible.")
        meta = extract_page_metadata(test_url)
        if meta and "snippet" in meta:
            print("🔎 Metadata:", meta)
            summary = check_relevance_with_ai(meta['snippet'], topic)
            print("🧠 Relevance summary:", summary)
        else:
            print("⚠️ No usable metadata or snippet found.")
    else:
        print("❌ URL not accessible.")

