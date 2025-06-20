"""
Google Search Service
---------------------
Fetches search results using Google's Custom Search JSON API.

Used by the Research Agent to gather real-world sources related to a content topic.
"""

import os
from typing import List, Dict
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()  # Loads from .env file

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

def get_google_search_results(query: str, limit: int = 10) -> List[Dict]:
    """
    Searches Google using the Custom Search API and returns cleaned results.

    Args:
        query (str): The refined topic or search query.
        limit (int): Total number of results to return (max 50).

    Returns:
        List[Dict]: List of results with keys: title, url, snippet
    """
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        print("⚠️ Missing Google API key or search engine ID")
        return []

    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    all_results = []
    seen_urls = set()
    start_index = 1

    while len(all_results) < limit:
        num = min(10, limit - len(all_results))
        try:
            response = service.cse().list(
                q=query,
                cx=GOOGLE_CSE_ID,
                num=num,
                start=start_index,
            ).execute()

            items = response.get("items", [])
            if not items:
                break

            for item in items:
                url = item.get("link")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    all_results.append({
                        "title": item.get("title", ""),
                        "url": url,
                        "snippet": item.get("snippet", "")
                    })

            start_index += num

        except Exception as e:
            print(f"❌ Google Search API error: {e}")
            break

    print(f"✅ Google search returned {len(all_results)} unique results")
    return all_results

# Test block to run manually
if __name__ == "__main__":
    query = "The impact of AI on medical diagnostics"
    results = get_google_search_results(query, limit=5)
    print("\n🔎 Sample Google Search Results:\n")
    for idx, r in enumerate(results, start=1):
        print(f"{idx}. {r['title']}\n   {r['url']}\n   {r['snippet']}\n")