#!/usr/bin/env python3
"""
Quick test script to verify TwitterAPI provider functionality.
Tests the hook with real API calls.
"""

import os
import sys

# Ensure the provider is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unittest.mock import Mock

from airflow_provider_twitterapi.hooks.twitterapi import TwitterApiHook


def test_twitterapi_connection():
    """Test TwitterAPI connection with the provided API key."""

    # Create a mock connection
    mock_conn = Mock()
    mock_conn.password = "new1_b099c7579e9444ec89d1c0fdcf7c2905"
    mock_conn.extra_dejson = {}

    # Create hook and patch the connection
    hook = TwitterApiHook(twitterapi_conn_id="test")
    hook.get_connection = lambda conn_id: mock_conn

    print("=" * 60)
    print("Testing TwitterAPI Provider")
    print("=" * 60)

    # Test 1: Get user by username
    print("\n1. Testing get_user_by_username...")
    try:
        result = hook.get_user_by_username(username="KaitoEasyAPI")
        print("✓ Success! User data retrieved:")
        print(f"  Username: {result.get('data', {}).get('username', 'N/A')}")
        print(f"  Name: {result.get('data', {}).get('name', 'N/A')}")
        print(f"  User ID: {result.get('data', {}).get('userId', 'N/A')}")
    except Exception as e:
        print(f"✗ Failed: {str(e)}")
        return False

    # Test 2: Search tweets
    print("\n2. Testing search_tweets...")
    try:
        result = hook.search_tweets(
            query="python",
            start_date="2024-12-01",
            end_date="2024-12-08",
            max_results=10,
        )
        tweet_count = len(result.get("data", []))
        print(f"✓ Success! Found {tweet_count} tweets")
        if tweet_count > 0:
            first_tweet = result.get("data", [])[0]
            print(f"  First tweet text: {first_tweet.get('text', 'N/A')[:100]}...")
    except Exception as e:
        print(f"✗ Failed: {str(e)}")
        return False

    # Test 3: Get user followers
    print("\n3. Testing get_user_followers...")
    try:
        result = hook.get_user_followers(username="KaitoEasyAPI", max_results=10)
        follower_count = len(result.get("data", []))
        print(f"✓ Success! Retrieved {follower_count} followers")
    except Exception as e:
        print(f"✗ Failed: {str(e)}")
        return False

    # Test 4: Get user tweets
    print("\n4. Testing get_user_tweets...")
    try:
        result = hook.get_user_tweets(username="KaitoEasyAPI", max_results=10)
        tweet_count = len(result.get("data", []))
        print(f"✓ Success! Retrieved {tweet_count} tweets from user")
    except Exception as e:
        print(f"✗ Failed: {str(e)}")
        return False

    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_twitterapi_connection()
    sys.exit(0 if success else 1)
