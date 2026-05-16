"""TwitterAPI.io Operators for Apache Airflow."""

from __future__ import annotations

from typing import Any

from airflow.models import BaseOperator

from airflow_provider_twitterapi.hooks.twitterapi import TwitterApiHook


class TwitterGetTweetByIdsOperator(BaseOperator):
    """
    Operator to get tweet details by tweet IDs.

    :param tweet_ids: List of tweet IDs to retrieve
    :param twitterapi_conn_id: The connection ID to use
    :param api_provider: Optional backend, "twitterapi_io" or "xquik"
    """

    template_fields = ("tweet_ids",)

    def __init__(
        self,
        *,
        tweet_ids: list[str],
        twitterapi_conn_id: str = "twitterapi_default",
        api_provider: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.tweet_ids = tweet_ids
        self.twitterapi_conn_id = twitterapi_conn_id
        self.api_provider = api_provider

    def execute(self, context: Any) -> dict[str, Any]:
        """Execute the operator."""
        hook = TwitterApiHook(
            twitterapi_conn_id=self.twitterapi_conn_id,
            api_provider=self.api_provider,
        )
        self.log.info(f"Fetching tweets: {self.tweet_ids}")
        return hook.get_tweet_by_ids(self.tweet_ids)


class TwitterGetUserByUsernameOperator(BaseOperator):
    """
    Operator to get user profile by username.

    :param username: Twitter username (without @)
    :param twitterapi_conn_id: The connection ID to use
    :param api_provider: Optional backend, "twitterapi_io" or "xquik"
    """

    template_fields = ("username",)

    def __init__(
        self,
        *,
        username: str,
        twitterapi_conn_id: str = "twitterapi_default",
        api_provider: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.username = username
        self.twitterapi_conn_id = twitterapi_conn_id
        self.api_provider = api_provider

    def execute(self, context: Any) -> dict[str, Any]:
        """Execute the operator."""
        hook = TwitterApiHook(
            twitterapi_conn_id=self.twitterapi_conn_id,
            api_provider=self.api_provider,
        )
        self.log.info(f"Fetching user profile: {self.username}")
        return hook.get_user_by_username(self.username)


class TwitterGetUserByUserIdsOperator(BaseOperator):
    """
    Operator to get user profiles by user IDs.

    :param user_ids: List of user IDs to retrieve
    :param twitterapi_conn_id: The connection ID to use
    :param api_provider: Optional backend, "twitterapi_io" or "xquik"
    """

    template_fields = ("user_ids",)

    def __init__(
        self,
        *,
        user_ids: list[str],
        twitterapi_conn_id: str = "twitterapi_default",
        api_provider: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.user_ids = user_ids
        self.twitterapi_conn_id = twitterapi_conn_id
        self.api_provider = api_provider

    def execute(self, context: Any) -> dict[str, Any]:
        """Execute the operator."""
        hook = TwitterApiHook(
            twitterapi_conn_id=self.twitterapi_conn_id,
            api_provider=self.api_provider,
        )
        self.log.info(f"Fetching user profiles: {self.user_ids}")
        return hook.get_user_by_userids(self.user_ids)


class TwitterSearchTweetsOperator(BaseOperator):
    """
    Operator to search tweets with advanced filters.

    :param query: Search query (e.g., "AI" OR "Twitter" from:elonmusk)
    :param query_type: Query type - "Latest" or "Top" (default: "Latest")
    :param cursor: Cursor for pagination (empty string for first page)
    :param twitterapi_conn_id: The connection ID to use
    :param api_provider: Optional backend, "twitterapi_io" or "xquik"
    """

    template_fields = ("query", "cursor")

    def __init__(
        self,
        *,
        query: str,
        query_type: str = "Latest",
        cursor: str | None = None,
        twitterapi_conn_id: str = "twitterapi_default",
        api_provider: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.query = query
        self.query_type = query_type
        self.cursor = cursor
        self.twitterapi_conn_id = twitterapi_conn_id
        self.api_provider = api_provider

    def execute(self, context: Any) -> dict[str, Any]:
        """Execute the operator."""
        hook = TwitterApiHook(
            twitterapi_conn_id=self.twitterapi_conn_id,
            api_provider=self.api_provider,
        )
        self.log.info(f"Searching tweets: {self.query}")
        return hook.search_tweets(
            query=self.query,
            query_type=self.query_type,
            cursor=self.cursor,
        )


class TwitterGetUserFollowersOperator(BaseOperator):
    """
    Operator to get followers list for a user.

    :param username: Twitter username (without @)
    :param cursor: Cursor for pagination (empty string for first page)
    :param page_size: Number of followers per page (20-200, default: 200)
    :param twitterapi_conn_id: The connection ID to use
    :param api_provider: Optional backend, "twitterapi_io" or "xquik"
    """

    template_fields = ("username", "cursor")

    def __init__(
        self,
        *,
        username: str,
        cursor: str | None = None,
        page_size: int = 200,
        twitterapi_conn_id: str = "twitterapi_default",
        api_provider: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.username = username
        self.cursor = cursor
        self.page_size = page_size
        self.twitterapi_conn_id = twitterapi_conn_id
        self.api_provider = api_provider

    def execute(self, context: Any) -> dict[str, Any]:
        """Execute the operator."""
        hook = TwitterApiHook(
            twitterapi_conn_id=self.twitterapi_conn_id,
            api_provider=self.api_provider,
        )
        self.log.info(f"Fetching followers for: {self.username}")
        return hook.get_user_followers(
            username=self.username,
            cursor=self.cursor,
            page_size=self.page_size,
        )


class TwitterGetUserFollowingsOperator(BaseOperator):
    """
    Operator to get following list for a user.

    :param username: Twitter username (without @)
    :param cursor: Cursor for pagination (empty string for first page)
    :param page_size: Number of followings per page (20-200, default: 200)
    :param twitterapi_conn_id: The connection ID to use
    :param api_provider: Optional backend, "twitterapi_io" or "xquik"
    """

    template_fields = ("username", "cursor")

    def __init__(
        self,
        *,
        username: str,
        cursor: str | None = None,
        page_size: int = 200,
        twitterapi_conn_id: str = "twitterapi_default",
        api_provider: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.username = username
        self.cursor = cursor
        self.page_size = page_size
        self.twitterapi_conn_id = twitterapi_conn_id
        self.api_provider = api_provider

    def execute(self, context: Any) -> dict[str, Any]:
        """Execute the operator."""
        hook = TwitterApiHook(
            twitterapi_conn_id=self.twitterapi_conn_id,
            api_provider=self.api_provider,
        )
        self.log.info(f"Fetching followings for: {self.username}")
        return hook.get_user_followings(
            username=self.username,
            cursor=self.cursor,
            page_size=self.page_size,
        )


class TwitterGetUserTweetsOperator(BaseOperator):
    """
    Operator to get tweets from a user's timeline.

    :param user_id: Twitter user ID (recommended, more stable and faster)
    :param username: Twitter username (without @)
    :param cursor: Cursor for pagination (empty string for first page)
    :param include_replies: Whether to include replies (default: False)
    :param twitterapi_conn_id: The connection ID to use
    :param api_provider: Optional backend, "twitterapi_io" or "xquik"

    Note: Either user_id or username must be provided. If both are provided,
          user_id will be used.
    """

    template_fields = ("user_id", "username", "cursor")

    def __init__(
        self,
        *,
        user_id: str | None = None,
        username: str | None = None,
        cursor: str | None = None,
        include_replies: bool = False,
        twitterapi_conn_id: str = "twitterapi_default",
        api_provider: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.user_id = user_id
        self.username = username
        self.cursor = cursor
        self.include_replies = include_replies
        self.twitterapi_conn_id = twitterapi_conn_id
        self.api_provider = api_provider

    def execute(self, context: Any) -> dict[str, Any]:
        """Execute the operator."""
        hook = TwitterApiHook(
            twitterapi_conn_id=self.twitterapi_conn_id,
            api_provider=self.api_provider,
        )
        self.log.info(
            f"Fetching tweets for user_id={self.user_id}, username={self.username}"
        )
        return hook.get_user_tweets(
            user_id=self.user_id,
            username=self.username,
            cursor=self.cursor,
            include_replies=self.include_replies,
        )


class TwitterSearchUserTweetsByDateOperator(BaseOperator):
    """
    Operator to search tweets from a specific user within a date range.

    :param username: Twitter username (without @)
    :param since: Start date (YYYY-MM-DD format)
    :param until: End date (YYYY-MM-DD format)
    :param cursor: Cursor for pagination (empty string for first page)
    :param query_type: Query type - "Latest" or "Top" (default: "Latest")
    :param additional_filters: Additional search filters
        (e.g., "lang:en -filter:replies")
    :param twitterapi_conn_id: The connection ID to use
    :param api_provider: Optional backend, "twitterapi_io" or "xquik"
    """

    template_fields = (
        "username",
        "since",
        "until",
        "cursor",
        "additional_filters",
    )

    def __init__(
        self,
        *,
        username: str,
        since: str,
        until: str,
        cursor: str | None = None,
        query_type: str = "Latest",
        additional_filters: str = "",
        twitterapi_conn_id: str = "twitterapi_default",
        api_provider: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.username = username
        self.since = since
        self.until = until
        self.cursor = cursor
        self.query_type = query_type
        self.additional_filters = additional_filters
        self.twitterapi_conn_id = twitterapi_conn_id
        self.api_provider = api_provider

    def execute(self, context: Any) -> dict[str, Any]:
        """Execute the operator."""
        hook = TwitterApiHook(
            twitterapi_conn_id=self.twitterapi_conn_id,
            api_provider=self.api_provider,
        )
        self.log.info(
            f"Searching tweets from @{self.username} "
            f"between {self.since} and {self.until}"
        )
        return hook.search_user_tweets_by_date(
            username=self.username,
            since=self.since,
            until=self.until,
            cursor=self.cursor,
            query_type=self.query_type,
            additional_filters=self.additional_filters,
        )
