# Airflow Provider for TwitterAPI.io

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Apache Airflow 2.11+](https://img.shields.io/badge/airflow-2.11+-blue.svg)](https://airflow.apache.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

A comprehensive Apache Airflow provider for [TwitterAPI.io](https://twitterapi.io),
enabling seamless integration of Twitter data into your Airflow workflows. The
same hook and operators can also use [Xquik](https://xquik.com/api/v1) as an
optional X/Twitter API backend.

## Features

- **Complete API Coverage**: Access tweets, user profiles, followers, followings, and advanced search
- **Date Range Search**: Search tweets from specific users within custom date ranges
- **Airflow 2.11+ Compatible**: Built for the latest Airflow features
- **Type-Safe**: Full type hints with Python 3.9+
- **Easy Authentication**: Simple API key-based authentication via Airflow connections
- **Optional Xquik Backend**: Use the existing hook and operators with
  `api_provider="xquik"`
- **Production Ready**: Proper error handling, logging, and retry mechanisms

## Installation

```bash
pip install airflow-provider-twitterapi
```

Or install from source:

```bash
git clone https://github.com/hiyenwong/apache-airflow-provider-twitterapi.git
cd apache-airflow-provider-twitterapi
pip install -e .
```

## Quick Start

### 1. Configure Connection

In Airflow UI, create a new connection:

- **Connection ID**: `twitterapi_default`
- **Connection Type**: `TwitterAPI.io`
- **Password**: Your TwitterAPI.io API key (get it from [TwitterAPI.io Dashboard](https://twitterapi.io/dashboard))

Or via CLI:

```bash
airflow connections add twitterapi_default \
    --conn-type twitterapi \
    --conn-password YOUR_API_KEY
```

To use Xquik instead of TwitterAPI.io, keep the same connection type and set the
provider in connection extra:

```bash
airflow connections add xquik_default \
    --conn-type twitterapi \
    --conn-password YOUR_XQUIK_API_KEY \
    --conn-extra '{"api_provider": "xquik"}'
```

### 2. Use in Your DAG

```python
from datetime import datetime
from airflow import DAG
from airflow_provider_twitterapi.operators.twitterapi import (
    TwitterGetUserByUsernameOperator,
    TwitterSearchTweetsOperator,
    TwitterSearchUserTweetsByDateOperator,
)

with DAG(
    dag_id="twitter_example",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
) as dag:

    # Get user profile
    get_user = TwitterGetUserByUsernameOperator(
        task_id="get_user",
        username="elonmusk",
    )

    # Search tweets
    search = TwitterSearchTweetsOperator(
        task_id="search_tweets",
        query="python airflow",
        query_type="Latest",
    )

    # Search user tweets by date range
    search_by_date = TwitterSearchUserTweetsByDateOperator(
        task_id="search_by_date",
        username="elonmusk",
        since="2024-01-01",
        until="2024-01-31",
    )
```

## Available Operators

### TwitterGetUserByUsernameOperator
Get user profile information by username.

```python
get_user = TwitterGetUserByUsernameOperator(
    task_id="get_user",
    username="KaitoEasyAPI",
)
```

To use Xquik for one task without changing the connection extra, pass
`api_provider="xquik"`:

```python
get_user = TwitterGetUserByUsernameOperator(
    task_id="get_user_xquik",
    username="xquikcom",
    twitterapi_conn_id="xquik_default",
    api_provider="xquik",
)
```

### TwitterGetTweetByIdsOperator
Retrieve tweet details by tweet IDs.

```python
get_tweets = TwitterGetTweetByIdsOperator(
    task_id="get_tweets",
    tweet_ids=["1234567890", "0987654321"],
)
```

### TwitterSearchTweetsOperator
Advanced tweet search with filters.

```python
search = TwitterSearchTweetsOperator(
    task_id="search",
    query="python airflow",
    query_type="Latest",  # "Latest" or "Top"
    cursor=None,  # For pagination
)
```

### TwitterGetUserFollowersOperator
Get followers list for a user.

```python
get_followers = TwitterGetUserFollowersOperator(
    task_id="get_followers",
    username="elonmusk",
    page_size=200,  # 20-200, default: 200
    cursor=None,  # For pagination
)
```

### TwitterGetUserFollowingsOperator
Get following list for a user.

```python
get_followings = TwitterGetUserFollowingsOperator(
    task_id="get_followings",
    username="elonmusk",
    page_size=200,  # 20-200, default: 200
    cursor=None,  # For pagination
)
```

### TwitterGetUserTweetsOperator
Get tweets from a user's timeline.

```python
get_tweets = TwitterGetUserTweetsOperator(
    task_id="get_user_tweets",
    username="elonmusk",  # Or use user_id="123456789"
    include_replies=False,
    cursor=None,  # For pagination
)
```

### TwitterSearchUserTweetsByDateOperator
Search tweets from a specific user within a date range.

```python
search_by_date = TwitterSearchUserTweetsByDateOperator(
    task_id="search_by_date",
    username="elonmusk",
    since="2024-01-01",
    until="2024-01-31",
    query_type="Latest",  # "Latest" or "Top"
    additional_filters="",  # Optional: "lang:en -filter:replies"
)
```

## Using the Hook Directly

For more complex workflows, use the `TwitterApiHook` directly:

```python
from airflow_provider_twitterapi.hooks.twitterapi import TwitterApiHook

hook = TwitterApiHook(twitterapi_conn_id="twitterapi_default")

# Get user profile
user_data = hook.get_user_by_username("elonmusk")

# Search tweets
tweets = hook.search_tweets(
    query="python",
    query_type="Latest",
)

# Search user tweets by date range
user_tweets = hook.search_user_tweets_by_date(
    username="elonmusk",
    since="2024-01-01",
    until="2024-01-31",
    additional_filters="lang:en",
)
```

Use Xquik directly through the hook:

```python
hook = TwitterApiHook(
    twitterapi_conn_id="xquik_default",
    api_provider="xquik",
)

tweets = hook.search_tweets(query="from:xquikcom")
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/apache-airflow-provider-twitterapi.git
cd apache-airflow-provider-twitterapi

# Install with dev dependencies
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black .

# Lint
ruff check .

# Type check
mypy airflow_provider_twitterapi/
```

## Project Structure

```
airflow-provider-twitterapi/
├── airflow_provider_twitterapi/
│   ├── __init__.py
│   ├── provider.yaml          # Provider metadata
│   ├── hooks/
│   │   ├── __init__.py
│   │   └── twitterapi.py      # TwitterApiHook
│   ├── operators/
│   │   ├── __init__.py
│   │   └── twitterapi.py      # All operators
│   └── sensors/
│       └── __init__.py
├── examples/
│   └── example_twitterapi_dag.py
├── pyproject.toml
└── README.md
```

## API Documentation

For detailed API documentation, visit [TwitterAPI.io Docs](https://docs.twitterapi.io/).

For the optional Xquik backend, see
[Xquik API Docs](https://docs.xquik.com/api-reference/overview).

## Pricing

TwitterAPI.io offers competitive pricing:
- $0.15/1k tweets
- $0.18/1k user profiles
- $0.15/1k followers
- Minimum charge: $0.00015 per request

Special discounts available for students and research institutions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

## Support

- Documentation: https://docs.twitterapi.io/
- Issues: https://github.com/hiyenwong/apache-airflow-provider-twitterapi/issues
