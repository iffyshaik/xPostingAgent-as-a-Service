# app/tests/test_platform_publisher.py

"""
Unit tests for platform_publisher.py
Covers: Typefully integration (success + failure)
"""

import pytest
from unittest.mock import patch
from app.services.platform_publisher import post_to_typefully
from datetime import datetime

# --- Success case ---
@patch("app.services.platform_publisher.requests.post")
def test_post_to_typefully_success(mock_post):
    mock_response = mock_post.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "draft123"}

    content = "Test tweet\nSecond line"
    scheduled = datetime.utcnow()

    result = post_to_typefully(content, scheduled_for=scheduled)

    assert result["platform_posted_id"] == "draft123"
    assert "post_response" in result
    assert mock_post.called

# --- 400 error case ---
@patch("app.services.platform_publisher.requests.post")
def test_post_to_typefully_failure(mock_post):
    mock_response = mock_post.return_value
    mock_response.status_code = 400
    mock_response.text = '{"detail":"Invalid payload"}'

    with pytest.raises(Exception) as e:
        post_to_typefully("Bad content")

    assert "Typefully API error 400" in str(e.value)
