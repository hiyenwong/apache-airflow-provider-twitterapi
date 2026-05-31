"""TwitterAPI.io Hook for Apache Airflow."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

import requests
from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook

TWITTERAPI_IO_PROVIDER = "twitterapi_io"
GETXAPI_PROVIDER = "getxapi"
DEFAULT_TWITTERAPI_IO_BASE_URL = "https://api.twitterapi.io"
DEFAULT_GETXAPI_BASE_URL = "https://api.getxapi.com"


class TwitterApiHook(BaseHook):
    """
    Hook for interacting with TwitterAPI.io API.

    This hook handles authentication and provides methods to interact with
    various TwitterAPI.io endpoints.

    :param twitterapi_conn_id: The connection ID to use for authentication.
    :type twitterapi_conn_id: str
    :param api_provider: API backend to use. Supported values are
        "twitterapi_io" and "getxapi". Connection extra can also set
        {"api_provider": "getxapi"}.
    :type api_provider: str | None
    :param base_url: Optional API base URL override.
    :type base_url: str | None
    """

    conn_name_attr = "twitterapi_conn_id"
    default_conn_name = "twitterapi_default"
    conn_type = "twitterapi"
    hook_name = "TwitterAPI.io"

    def __init__(
        self,
        twitterapi_conn_id: str = default_conn_name,
        api_provider: str | None = None,
        base_url: str | None = None,
    ) -> None:
        super().__init__()
        self.twitterapi_conn_id = twitterapi_conn_id
        self._api_provider = self._normalize_api_provider(api_provider)
        self._base_url_override = base_url.rstrip("/") if base_url else None
        self.base_url = self._default_base_url(self._api_provider)
        self._api_key: str | None = None
        self._conn_extra: dict[str, Any] = {}

    @staticmethod
    def _normalize_api_provider(provider: str | None) -> str | None:
        """Normalize API provider aliases."""
        if provider is None or not str(provider).strip():
            return None

        normalized = str(provider).strip().lower().replace("-", "_")
        if normalized in {"twitterapi", "twitterapi.io", TWITTERAPI_IO_PROVIDER}:
            return TWITTERAPI_IO_PROVIDER
        if normalized in {GETXAPI_PROVIDER, "getxapi.com", "get_xapi"}:
            return GETXAPI_PROVIDER

        raise AirflowException(
            "Unsupported API provider. Use 'twitterapi_io' or 'getxapi'."
        )

    @staticmethod
    def _default_base_url(provider: str | None) -> str:
        """Return the default base URL for an API provider."""
        if provider == GETXAPI_PROVIDER:
            return DEFAULT_GETXAPI_BASE_URL
        return DEFAULT_TWITTERAPI_IO_BASE_URL

    def _get_api_provider(self) -> str:
        """Return the configured API provider, loading connection extra if needed."""
        if not self._api_provider:
            self.get_conn()
        return self._api_provider or TWITTERAPI_IO_PROVIDER

    @staticmethod
    def _path_part(value: str) -> str:
        """Escape a user or tweet identifier for use in an endpoint path."""
        return quote(value.lstrip("@"), safe="")

    def get_conn(self) -> str:
        """
        Get the API key from the connection.

        :return: API key for authentication
        :rtype: str
        """
        if self._api_key:
            return self._api_key

        conn = self.get_connection(self.twitterapi_conn_id)
        self._conn_extra = conn.extra_dejson or {}

        if not self._api_provider:
            self._api_provider = self._normalize_api_provider(
                self._conn_extra.get("api_provider")
                or self._conn_extra.get("provider")
                or TWITTERAPI_IO_PROVIDER
            )

        base_url = self._base_url_override or self._conn_extra.get("base_url")
        if base_url:
            self.base_url = str(base_url).strip().rstrip("/")
        else:
            self.base_url = self._default_base_url(self._api_provider)

        # API key can be stored in password field or in extra
        if conn.password:
            self._api_key = conn.password
        elif conn.extra_dejson.get("api_key"):
            self._api_key = conn.extra_dejson.get("api_key")
        else:
            raise AirflowException(
                f"Missing API key in connection '{self.twitterapi_conn_id}'. "
                "Please provide API key in password field or extra as 'api_key'."
            )

        return self._api_key

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Make an HTTP request to the configured API.

        :param method: HTTP method (GET, POST, etc.)
        :param endpoint: API endpoint path
        :param params: Query parameters
        :param json_data: JSON data for POST requests
        :return: Response JSON
        :raises AirflowException: If the request fails
        """
        api_key = self.get_conn()
        url = f"{self.base_url}{endpoint}"
        if self._get_api_provider() == GETXAPI_PROVIDER:
            headers = {"Authorization": f"Bearer {api_key}"}
        else:
            headers = {"x-api-key": api_key}

        self.log.info(f"Making {method} request to {url}")

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_data,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise AirflowException(f"HTTP error occurred: {e.response.text}") from e
        except requests.exceptions.RequestException as e:
            raise AirflowException(f"Request failed: {str(e)}") from e

    def get_tweet_by_ids(self, tweet_ids: list[str]) -> dict[str, Any]:
        """
        Get tweet details by tweet IDs.

        :param tweet_ids: List of tweet IDs
        :return: Tweet data
        """
        if self._get_api_provider() == GETXAPI_PROVIDER:
            params = {"ids": ",".join(tweet_ids)}
            return self._make_request("GET", "/twitter/tweets", params=params)

        params = {"tweet_ids": ",".join(tweet_ids)}
        return self._make_request("GET", "/twitter/tweets", params=params)

    def get_user_by_username(self, username: str) -> dict[str, Any]:
        """
        Get user profile by username.

        :param username: Twitter username (without @)
        :return: User profile data
        """
        if self._get_api_provider() == GETXAPI_PROVIDER:
            return self._make_request(
                "GET", f"/twitter/users/{self._path_part(username)}"
            )

        params = {"userName": username}
        return self._make_request("GET", "/twitter/user/info", params=params)

    def get_user_by_userids(self, user_ids: list[str]) -> dict[str, Any]:
        """
        Get user profiles by user IDs.

        :param user_ids: List of user IDs
        :return: User profiles data
        """
        if self._get_api_provider() == GETXAPI_PROVIDER:
            params = {"ids": ",".join(user_ids)}
            return self._make_request("GET", "/twitter/users/batch", params=params)

        params = {"userIds": ",".join(user_ids)}
        return self._make_request(
            "GET", "/twitter/user/batch_info_by_ids", params=params
        )

    def search_tweets(
        self,
        query: str,
        query_type: str = "Latest",
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """
        Advanced tweet search with filters.

        :param query: Search query (e.g., "AI" OR "Twitter" from:elonmusk)
        :param query_type: Query type - "Latest" or "Top" (default: "Latest")
        :param cursor: Cursor for pagination (empty string for first page)
        :return: Search results with tweets, has_next_page, and next_cursor
        """
        if self._get_api_provider() == GETXAPI_PROVIDER:
            params: dict[str, Any] = {"q": query, "queryType": query_type}
            if cursor is not None:
                params["cursor"] = cursor
            return self._make_request(
                "GET", "/twitter/tweet/advanced_search", params=params
            )

        params: dict[str, Any] = {"query": query, "queryType": query_type}
        if cursor is not None:
            params["cursor"] = cursor

        return self._make_request(
            "GET", "/twitter/tweet/advanced_search", params=params
        )

    def get_user_followers(
        self,
        username: str,
        cursor: str | None = None,
        page_size: int = 200,
    ) -> dict[str, Any]:
        """
        Get followers list for a user.

        :param username: Twitter username (without @)
        :param cursor: Cursor for pagination (empty string for first page)
        :param page_size: Number of followers per page (20-200, default: 200)
        :return: Followers data with followers array, has_next_page, next_cursor
        """
        if self._get_api_provider() == GETXAPI_PROVIDER:
            params: dict[str, Any] = {"pageSize": page_size}
            if cursor is not None:
                params["cursor"] = cursor
            return self._make_request(
                "GET",
                f"/twitter/users/{self._path_part(username)}/followers",
                params=params,
            )

        params: dict[str, Any] = {"userName": username, "pageSize": page_size}
        if cursor is not None:
            params["cursor"] = cursor

        return self._make_request("GET", "/twitter/user/followers", params=params)

    def get_user_followings(
        self,
        username: str,
        cursor: str | None = None,
        page_size: int = 200,
    ) -> dict[str, Any]:
        """
        Get following list for a user.

        :param username: Twitter username (without @)
        :param cursor: Cursor for pagination (empty string for first page)
        :param page_size: Number of followings per page (20-200, default: 200)
        :return: Following data with followings array, has_next_page, next_cursor
        """
        if self._get_api_provider() == GETXAPI_PROVIDER:
            params: dict[str, Any] = {"pageSize": page_size}
            if cursor is not None:
                params["cursor"] = cursor
            return self._make_request(
                "GET",
                f"/twitter/users/{self._path_part(username)}/following",
                params=params,
            )

        params: dict[str, Any] = {"userName": username, "pageSize": page_size}
        if cursor is not None:
            params["cursor"] = cursor

        return self._make_request("GET", "/twitter/user/followings", params=params)

    def get_user_tweets(
        self,
        user_id: str | None = None,
        username: str | None = None,
        cursor: str | None = None,
        include_replies: bool = False,
    ) -> dict[str, Any]:
        """
        Get tweets from a user's timeline.

        :param user_id: Twitter user ID (recommended, more stable and faster)
        :param username: Twitter username (without @)
        :param cursor: Cursor for pagination (empty string for first page)
        :param include_replies: Whether to include replies (default: False)
        :return: User tweets data with tweets array, has_next_page, next_cursor

        Note: userId and userName are mutually exclusive. If both are provided,
              userId will be used.
        """
        if self._get_api_provider() == GETXAPI_PROVIDER:
            identifier = user_id or username
            if not identifier:
                raise AirflowException("Either user_id or username must be provided")

            params: dict[str, Any] = {"includeReplies": str(include_replies).lower()}
            if cursor is not None:
                params["cursor"] = cursor
            return self._make_request(
                "GET",
                f"/twitter/users/{self._path_part(identifier)}/tweets",
                params=params,
            )

        params: dict[str, Any] = {"includeReplies": str(include_replies).lower()}
        if user_id:
            params["userId"] = user_id
        elif username:
            params["userName"] = username
        else:
            raise AirflowException("Either user_id or username must be provided")

        if cursor is not None:
            params["cursor"] = cursor

        return self._make_request("GET", "/twitter/user/last_tweets", params=params)

    def search_user_tweets_by_date(
        self,
        username: str,
        since: str,
        until: str,
        cursor: str | None = None,
        query_type: str = "Latest",
        additional_filters: str = "",
    ) -> dict[str, Any]:
        """
        Search tweets from a specific user within a date range.

        :param username: Twitter username (without @)
        :param since: Start date (YYYY-MM-DD format)
        :param until: End date (YYYY-MM-DD format)
        :param cursor: Cursor for pagination (empty string for first page)
        :param query_type: Query type - "Latest" or "Top" (default: "Latest")
        :param additional_filters: Additional search filters
            (e.g., "lang:en -filter:replies")
        :return: Search results with tweets, has_next_page, and next_cursor

        Example:
            >>> hook = TwitterApiHook()
            >>> result = hook.search_user_tweets_by_date(
            ...     username="elonmusk",
            ...     since="2024-01-01",
            ...     until="2024-01-31"
            ... )
        """
        query = f"from:{username} since:{since} until:{until}"
        if additional_filters:
            query = f"{query} {additional_filters}"

        return self.search_tweets(query=query, query_type=query_type, cursor=cursor)

    @classmethod
    def get_ui_field_behaviour(cls) -> dict[str, Any]:
        """Return custom field behaviour for the connection form in Airflow UI."""
        return {
            "hidden_fields": ["schema", "port", "host", "login"],
            "relabeling": {
                "password": "API Key",
                "extra": "Provider Options",
            },
            "placeholders": {
                "password": "TwitterAPI.io or GetXAPI API key",
                "extra": (
                    '{"api_provider": "twitterapi_io"} or '
                    '{"api_provider": "getxapi"}'
                ),
            },
        }
