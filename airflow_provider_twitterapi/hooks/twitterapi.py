"""TwitterAPI.io Hook for Apache Airflow."""

from __future__ import annotations

from typing import Any

import requests
from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook


class TwitterApiHook(BaseHook):
    """
    Hook for interacting with TwitterAPI.io API.

    This hook handles authentication and provides methods to interact with
    various TwitterAPI.io endpoints.

    :param twitterapi_conn_id: The connection ID to use for authentication.
    :type twitterapi_conn_id: str
    """

    conn_name_attr = "twitterapi_conn_id"
    default_conn_name = "twitterapi_default"
    conn_type = "twitterapi"
    hook_name = "TwitterAPI.io"

    def __init__(self, twitterapi_conn_id: str = default_conn_name) -> None:
        super().__init__()
        self.twitterapi_conn_id = twitterapi_conn_id
        self.base_url = "https://api.twitterapi.io"
        self._api_key: str | None = None

    def get_conn(self) -> str:
        """
        Get the API key from the connection.

        :return: API key for authentication
        :rtype: str
        """
        if self._api_key:
            return self._api_key

        conn = self.get_connection(self.twitterapi_conn_id)

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
        Make an HTTP request to the TwitterAPI.io API.

        :param method: HTTP method (GET, POST, etc.)
        :param endpoint: API endpoint path
        :param params: Query parameters
        :param json_data: JSON data for POST requests
        :return: Response JSON
        :raises AirflowException: If the request fails
        """
        api_key = self.get_conn()
        url = f"{self.base_url}{endpoint}"
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
        params = {"tweetIds": ",".join(tweet_ids)}
        return self._make_request("GET", "/twitter/tweet", params=params)

    def get_user_by_username(self, username: str) -> dict[str, Any]:
        """
        Get user profile by username.

        :param username: Twitter username (without @)
        :return: User profile data
        """
        params = {"userName": username}
        return self._make_request("GET", "/twitter/user", params=params)

    def get_user_by_userids(self, user_ids: list[str]) -> dict[str, Any]:
        """
        Get user profiles by user IDs.

        :param user_ids: List of user IDs
        :return: User profiles data
        """
        params = {"userIds": ",".join(user_ids)}
        return self._make_request("GET", "/twitter/user/batch", params=params)

    def search_tweets(
        self,
        query: str,
        start_date: str | None = None,
        end_date: str | None = None,
        max_results: int | None = None,
    ) -> dict[str, Any]:
        """
        Advanced tweet search with filters.

        :param query: Search query
        :param start_date: Start date (YYYY-MM-DD)
        :param end_date: End date (YYYY-MM-DD)
        :param max_results: Maximum number of results
        :return: Search results
        """
        params = {"query": query}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if max_results:
            params["maxResults"] = max_results

        return self._make_request("GET", "/twitter/search", params=params)

    def get_user_followers(
        self, username: str, max_results: int | None = None
    ) -> dict[str, Any]:
        """
        Get followers list for a user.

        :param username: Twitter username (without @)
        :param max_results: Maximum number of results
        :return: Followers data
        """
        params = {"userName": username}
        if max_results:
            params["maxResults"] = max_results

        return self._make_request("GET", "/twitter/user/followers", params=params)

    def get_user_followings(
        self, username: str, max_results: int | None = None
    ) -> dict[str, Any]:
        """
        Get following list for a user.

        :param username: Twitter username (without @)
        :param max_results: Maximum number of results
        :return: Following data
        """
        params = {"userName": username}
        if max_results:
            params["maxResults"] = max_results

        return self._make_request("GET", "/twitter/user/followings", params=params)

    def get_user_tweets(
        self, username: str, max_results: int | None = None
    ) -> dict[str, Any]:
        """
        Get tweets from a user's timeline.

        :param username: Twitter username (without @)
        :param max_results: Maximum number of results
        :return: User tweets data
        """
        params = {"userName": username}
        if max_results:
            params["maxResults"] = max_results

        return self._make_request("GET", "/twitter/user/tweets", params=params)

    @staticmethod
    def get_ui_field_behaviour() -> dict[str, Any]:
        """Return custom field behaviour for the connection form in Airflow UI."""
        return {
            "hidden_fields": ["schema", "port", "host", "login", "extra"],
            "relabeling": {
                "password": "API Key",
            },
            "placeholders": {
                "password": "Your TwitterAPI.io API key (x-api-key)",
            },
        }
