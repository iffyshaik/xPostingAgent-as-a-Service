# app/services/platform_publisher.py

"""
Handles publishing content to external platforms (Typefully, X).
Used by post_content in content_queue.py service.
"""

import requests
import json
from datetime import datetime
from app.config import settings

# --------------------------
# Typefully Integration
# --------------------------

def post_to_typefully(content: str, scheduled_for: datetime = None):
    """
    Posts content to Typefully via draft endpoint.
    """
    url = "https://api.typefully.com/v1/drafts/"
    headers = {
        "X-API-KEY": f"Bearer {settings.typefully_api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "content": content,
        "threadify": False,
        "share": True
    }

    if scheduled_for:
        payload["schedule-date"] = scheduled_for.isoformat()

    print("🔍 Posting to Typefully:")
    print("🔸 Headers:", headers)
    print("🔸 Payload:", payload)


    response = requests.post(url, headers=headers, json=payload)

    if response.status_code >= 400:
        raise Exception(f"Typefully API error {response.status_code}: {response.text}")

    result = response.json()
    return {
        "platform_posted_id": result.get("id", None),
        "post_response": json.dumps(result)
    }



# --------------------------
# Twitter (X) Integration
# --------------------------

def post_to_x(text: str, access_token: str, in_reply_to_id: str = None):
    """
    Posts a single tweet (or part of a thread) to X (Twitter).
    """
    url = "https://api.twitter.com/2/tweets"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {"text": text}
    if in_reply_to_id:
        payload["reply"] = {"in_reply_to_tweet_id": in_reply_to_id}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code >= 400:
        raise Exception(f"Twitter API error {response.status_code}: {response.text}")

    result = response.json()
    return {
        "platform_posted_id": result.get("data", {}).get("id", None),
        "post_response": json.dumps(result)
    }
