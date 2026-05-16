"""Tests for TwitterApiHook."""

from unittest.mock import Mock, patch

from airflow_provider_twitterapi.hooks.twitterapi import TwitterApiHook


class TestTwitterApiHook:
    """Test cases for TwitterApiHook."""

    @patch("airflow_provider_twitterapi.hooks.twitterapi.TwitterApiHook.get_connection")
    def test_get_conn_with_password(self, mock_get_connection):
        """Test getting API key from password field."""
        mock_conn = Mock()
        mock_conn.password = "test_api_key"
        mock_conn.extra_dejson = {}
        mock_get_connection.return_value = mock_conn

        hook = TwitterApiHook()
        api_key = hook.get_conn()

        assert api_key == "test_api_key"

    @patch("airflow_provider_twitterapi.hooks.twitterapi.TwitterApiHook.get_connection")
    def test_get_conn_with_extra(self, mock_get_connection):
        """Test getting API key from extra field."""
        mock_conn = Mock()
        mock_conn.password = None
        mock_conn.extra_dejson = {"api_key": "test_api_key_extra"}
        mock_get_connection.return_value = mock_conn

        hook = TwitterApiHook()
        api_key = hook.get_conn()

        assert api_key == "test_api_key_extra"

    @patch("airflow_provider_twitterapi.hooks.twitterapi.requests.request")
    @patch("airflow_provider_twitterapi.hooks.twitterapi.TwitterApiHook.get_connection")
    def test_make_request_success(self, mock_get_connection, mock_request):
        """Test successful API request."""
        mock_conn = Mock()
        mock_conn.password = "test_api_key"
        mock_conn.extra_dejson = {}
        mock_get_connection.return_value = mock_conn

        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_request.return_value = mock_response

        hook = TwitterApiHook()
        result = hook._make_request("GET", "/twitter/user", params={"userName": "test"})

        assert result == {"data": "test"}
        mock_request.assert_called_once()

    @patch("airflow_provider_twitterapi.hooks.twitterapi.requests.request")
    @patch("airflow_provider_twitterapi.hooks.twitterapi.TwitterApiHook.get_connection")
    def test_xquik_search_uses_xquik_endpoint_and_headers(
        self, mock_get_connection, mock_request
    ):
        """Test Xquik search request mapping."""
        mock_conn = Mock()
        mock_conn.password = "test_xquik_key"
        mock_conn.extra_dejson = {"api_provider": "xquik"}
        mock_get_connection.return_value = mock_conn

        mock_response = Mock()
        mock_response.json.return_value = {"tweets": []}
        mock_request.return_value = mock_response

        hook = TwitterApiHook()
        result = hook.search_tweets(
            query="from:xquikcom",
            query_type="Latest",
            cursor="next",
        )

        assert result == {"tweets": []}
        mock_request.assert_called_once_with(
            method="GET",
            url="https://xquik.com/api/v1/x/tweets/search",
            headers={
                "x-api-key": "test_xquik_key",
                "xquik-api-contract": "2026-04-29",
            },
            params={
                "q": "from:xquikcom",
                "queryType": "Latest",
                "cursor": "next",
            },
            json=None,
            timeout=30,
        )

    @patch("airflow_provider_twitterapi.hooks.twitterapi.requests.request")
    @patch("airflow_provider_twitterapi.hooks.twitterapi.TwitterApiHook.get_connection")
    def test_xquik_user_tweets_uses_username_path(
        self, mock_get_connection, mock_request
    ):
        """Test Xquik user timeline request mapping."""
        mock_conn = Mock()
        mock_conn.password = "test_xquik_key"
        mock_conn.extra_dejson = {}
        mock_get_connection.return_value = mock_conn

        mock_response = Mock()
        mock_response.json.return_value = {"tweets": []}
        mock_request.return_value = mock_response

        hook = TwitterApiHook(api_provider="xquik")
        result = hook.get_user_tweets(
            username="@xquikcom",
            cursor="cursor-1",
            include_replies=True,
        )

        assert result == {"tweets": []}
        mock_request.assert_called_once_with(
            method="GET",
            url="https://xquik.com/api/v1/x/users/xquikcom/tweets",
            headers={
                "x-api-key": "test_xquik_key",
                "xquik-api-contract": "2026-04-29",
            },
            params={
                "includeReplies": "true",
                "cursor": "cursor-1",
            },
            json=None,
            timeout=30,
        )
