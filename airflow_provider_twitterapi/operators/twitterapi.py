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
    """

    template_fields = ("tweet_ids",)

    def __init__(
        self,
        *,
        tweet_ids: list[str],
        twitterapi_conn_id: str = "twitterapi_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.tweet_ids = tweet_ids
        self.twitterapi_conn_id = twitterapi_conn_id

    def execute(self, context: Any) -> dict[str, Any]:
        """Execute the operator."""
        hook = TwitterApiHook(twitterapi_conn_id=self.twitterapi_conn_id)
        self.log.info(f"Fetching tweets: {self.tweet_ids}")
        return hook.get_tweet_by_ids(self.tweet_ids)


class TwitterGetUserByUsernameOperator(BaseOperator):
    """
    Operator to get user profile by username.

    :param username: Twitter username (without @)
    :param twitterapi_conn_id: The connection ID to use
    """

    template_fields = ("username",)

    def __init__(
        self,
        *,
        username: str,
        twitterapi_conn_id: str = "twitterapi_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.username = username
        self.twitterapi_conn_id = twitterapi_conn_id

    def execute(self, context: Any) -> dict[str, Any]:
        """Execute the operator."""
        hook = TwitterApiHook(twitterapi_conn_id=self.twitterapi_conn_id)
        self.log.info(f"Fetching user profile: {self.username}")
        return hook.get_user_by_username(self.username)


class TwitterGetUserByUserIdsOperator(BaseOperator):
    """
    Operator to get user profiles by user IDs.

    :param user_ids: List of user IDs to retrieve
    :param twitterapi_conn_id: The connection ID to use
    """

    template_fields = ("user_ids",)

    def __init__(
        self,
        *,
        user_ids: list[str],
        twitterapi_conn_id: str = "twitterapi_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.user_ids = user_ids
        self.twitterapi_conn_id = twitterapi_conn_id

    def execute(self, context: Any) -> dict[str, Any]:
        """Execute the operator."""
        hook = TwitterApiHook(twitterapi_conn_id=self.twitterapi_conn_id)
        self.log.info(f"Fetching user profiles: {self.user_ids}")
        return hook.get_user_by_userids(self.user_ids)


class TwitterSearchTweetsOperator(BaseOperator):
    """
    Operator to search tweets with advanced filters.

    :param query: Search query
    :param start_date: Start date (YYYY-MM-DD)
    :param end_date: End date (YYYY-MM-DD)
    :param max_results: Maximum number of results
    :param twitterapi_conn_id: The connection ID to use
    """

    template_fields = ("query", "start_date", "end_date")

    def __init__(
        self,
        *,
        query: str,
        start_date: str | None = None,
        end_date: str | None = None,
        max_results: int | None = None,
        twitterapi_conn_id: str = "twitterapi_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.query = query
        self.start_date = start_date
        self.end_date = end_date
        self.max_results = max_results
        self.twitterapi_conn_id = twitterapi_conn_id

    def execute(self, context: Any) -> dict[str, Any]:
        """Execute the operator."""
        hook = TwitterApiHook(twitterapi_conn_id=self.twitterapi_conn_id)
        self.log.info(f"Searching tweets: {self.query}")
        return hook.search_tweets(
            query=self.query,
            start_date=self.start_date,
            end_date=self.end_date,
            max_results=self.max_results,
        )


class TwitterGetUserFollowersOperator(BaseOperator):
    """
    Operator to get followers list for a user.

    :param username: Twitter username (without @)
    :param max_results: Maximum number of results
    :param twitterapi_conn_id: The connection ID to use
    """

    template_fields = ("username",)

    def __init__(
        self,
        *,
        username: str,
        max_results: int | None = None,
        twitterapi_conn_id: str = "twitterapi_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.username = username
        self.max_results = max_results
        self.twitterapi_conn_id = twitterapi_conn_id

    def execute(self, context: Any) -> dict[str, Any]:
        """Execute the operator."""
        hook = TwitterApiHook(twitterapi_conn_id=self.twitterapi_conn_id)
        self.log.info(f"Fetching followers for: {self.username}")
        return hook.get_user_followers(
            username=self.username, max_results=self.max_results
        )


class TwitterGetUserFollowingsOperator(BaseOperator):
    """
    Operator to get following list for a user.

    :param username: Twitter username (without @)
    :param max_results: Maximum number of results
    :param twitterapi_conn_id: The connection ID to use
    """

    template_fields = ("username",)

    def __init__(
        self,
        *,
        username: str,
        max_results: int | None = None,
        twitterapi_conn_id: str = "twitterapi_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.username = username
        self.max_results = max_results
        self.twitterapi_conn_id = twitterapi_conn_id

    def execute(self, context: Any) -> dict[str, Any]:
        """Execute the operator."""
        hook = TwitterApiHook(twitterapi_conn_id=self.twitterapi_conn_id)
        self.log.info(f"Fetching followings for: {self.username}")
        return hook.get_user_followings(
            username=self.username, max_results=self.max_results
        )


class TwitterGetUserTweetsOperator(BaseOperator):
    """
    Operator to get tweets from a user's timeline.

    :param username: Twitter username (without @)
    :param max_results: Maximum number of results
    :param twitterapi_conn_id: The connection ID to use
    """

    template_fields = ("username",)

    def __init__(
        self,
        *,
        username: str,
        max_results: int | None = None,
        twitterapi_conn_id: str = "twitterapi_default",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.username = username
        self.max_results = max_results
        self.twitterapi_conn_id = twitterapi_conn_id

    def execute(self, context: Any) -> dict[str, Any]:
        """Execute the operator."""
        hook = TwitterApiHook(twitterapi_conn_id=self.twitterapi_conn_id)
        self.log.info(f"Fetching tweets for: {self.username}")
        return hook.get_user_tweets(
            username=self.username, max_results=self.max_results
        )
