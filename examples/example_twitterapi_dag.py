"""
Example DAG demonstrating the TwitterAPI.io provider.

This DAG shows how to use various TwitterAPI.io operators to:
- Get user profiles
- Search tweets
- Retrieve user followers and followings
- Get user tweets
"""

from datetime import datetime, timedelta

from airflow import DAG

from airflow_provider_twitterapi.operators.twitterapi import (
    TwitterGetTweetByIdsOperator,
    TwitterGetUserByUsernameOperator,
    TwitterGetUserFollowersOperator,
    TwitterGetUserFollowingsOperator,
    TwitterGetUserTweetsOperator,
    TwitterSearchTweetsOperator,
)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="example_twitterapi_provider",
    default_args=default_args,
    description="Example DAG using TwitterAPI.io provider",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["example", "twitterapi"],
) as dag:
    # Get user profile by username
    get_user_profile = TwitterGetUserByUsernameOperator(
        task_id="get_user_profile",
        username="elonmusk",
        twitterapi_conn_id="twitterapi_default",
    )

    # Get user followers (pageSize: 20-200)
    get_followers = TwitterGetUserFollowersOperator(
        task_id="get_user_followers",
        username="elonmusk",
        page_size=100,
        twitterapi_conn_id="twitterapi_default",
    )

    # Get user followings (pageSize: 20-200)
    get_followings = TwitterGetUserFollowingsOperator(
        task_id="get_user_followings",
        username="elonmusk",
        page_size=100,
        twitterapi_conn_id="twitterapi_default",
    )

    # Get user tweets (can use user_id or username)
    get_user_tweets = TwitterGetUserTweetsOperator(
        task_id="get_user_tweets",
        username="elonmusk",
        include_replies=False,
        twitterapi_conn_id="twitterapi_default",
    )

    # Search tweets with advanced query
    # Query examples: "AI" OR "Twitter" from:elonmusk since:2021-12-31_23:59:59_UTC
    search_tweets = TwitterSearchTweetsOperator(
        task_id="search_tweets",
        query="from:elonmusk",
        query_type="Latest",  # "Latest" or "Top"
        twitterapi_conn_id="twitterapi_default",
    )

    # Get specific tweets by IDs (example IDs)
    get_tweets = TwitterGetTweetByIdsOperator(
        task_id="get_tweets_by_ids",
        tweet_ids=["1846987139428634858", "1866332309399781537"],
        twitterapi_conn_id="twitterapi_default",
    )

    # Define task dependencies
    get_user_profile >> [get_followers, get_followings, get_user_tweets]
    search_tweets >> get_tweets
