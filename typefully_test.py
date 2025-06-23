#!/usr/bin/env python3
"""
Simple script to post a tweet using Typefully API
"""

import requests
import json

# Configuration
API_KEY = "9bihkrIpqgUMkTD4"  # Get this from Typefully Settings > Integrations
API_BASE_URL = "https://api.typefully.com/v1"

def post_tweet(content, schedule_date=None, threadify=True, share=True):
    """
    Post a tweet using Typefully API
    
    Args:
        content (str): Tweet content
        schedule_date (str, optional): ISO date string or "next-free-slot" 
        threadify (bool): Auto-split into multiple tweets if needed
        share (bool): Whether to share the tweet
    
    Returns:
        dict: API response
    """
    
    url = f"{API_BASE_URL}/drafts/"
    
    headers = {
        "X-API-KEY": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "content": content,
        "threadify": threadify,
        "share": share
    }
    
    # Add schedule date if provided
    if schedule_date:
        payload["schedule-date"] = schedule_date
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        print("✅ Tweet posted successfully!")
        print(f"Response: {response.json()}")
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error posting tweet: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return None

def main():
    # Replace with your actual API key
    if API_KEY == "your_typefully_api_key_here":
        print("❌ Please set your Typefully API key in the script!")
        print("Get it from: https://typefully.com/?settings=integrations")
        return
    
    # Test tweet content
    tweet_content = """Hello from the Typefully API! 🚀

This is a test tweet posted programmatically using Python.

#API #Twitter #Automation"""
    
    print("📝 Posting tweet...")
    print(f"Content: {tweet_content}")
    print("-" * 50)
    
    # Post the tweet (will be published immediately)
    result = post_tweet(tweet_content)
    
    # Example of scheduling for later
    # result = post_tweet(tweet_content, schedule_date="next-free-slot")
    
    if result:
        print("🎉 Success! Check your Typefully dashboard.")

if __name__ == "__main__":
    main()