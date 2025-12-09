"""Test script for search_user_tweets_by_date functionality."""

from airflow_provider_twitterapi.hooks.twitterapi import TwitterApiHook


def test_search_user_tweets_by_date():
    """Test searching user tweets by date range."""
    # Initialize hook with default connection
    hook = TwitterApiHook(twitterapi_conn_id="twitterapi_default")

    print("Testing search_user_tweets_by_date()...")
    print("-" * 60)

    # Search tweets from @elonmusk in January 2024
    result = hook.search_user_tweets_by_date(
        username="elonmusk",
        since="2024-01-01",
        until="2024-01-31",
        query_type="Latest",
    )

    print("Search query: from:elonmusk since:2024-01-01 until:2024-01-31")
    print(f"Results received: {len(result.get('tweets', []))} tweets")
    print(f"Has next page: {result.get('has_next_page', False)}")

    if result.get("tweets"):
        print("\nFirst tweet:")
        first_tweet = result["tweets"][0]
        print(f"  Text: {first_tweet.get('text', 'N/A')[:100]}...")
        print(f"  Created at: {first_tweet.get('created_at', 'N/A')}")

    print("-" * 60)
    print("✅ Test completed successfully!")

    return result


if __name__ == "__main__":
    try:
        test_search_user_tweets_by_date()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
