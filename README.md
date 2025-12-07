# Apache Airflow Provider for TwitterAPI.io

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Apache Airflow 2.11+](https://img.shields.io/badge/airflow-2.11+-blue.svg)](https://airflow.apache.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

A comprehensive Apache Airflow provider for [TwitterAPI.io](https://twitterapi.io), enabling seamless integration of Twitter data into your Airflow workflows.

## Features

- **Complete API Coverage**: Access tweets, user profiles, followers, followings, and advanced search
- **Airflow 2.11+ Compatible**: Built for the latest Airflow features
- **Type-Safe**: Full type hints with Python 3.13+
- **Easy Authentication**: Simple API key-based authentication via Airflow connections
- **Production Ready**: Proper error handling, logging, and retry mechanisms

## Installation

```bash
pip install apache-airflow-provider-twitterapi
```

Or install from source:

```bash
git clone https://github.com/yourusername/apache-airflow-provider-twitterapi.git
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

### 2. Use in Your DAG

```python
from datetime import datetime
from airflow import DAG
from airflow_provider_twitterapi.operators.twitterapi import (
    TwitterGetUserByUsernameOperator,
    TwitterSearchTweetsOperator,
)

with DAG(
    dag_id="twitter_example",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
) as dag:

    # Get user profile
    get_user = TwitterGetUserByUsernameOperator(
        task_id="get_user",
        username="KaitoEasyAPI",
    )

    # Search tweets
    search = TwitterSearchTweetsOperator(
        task_id="search_tweets",
        query="python airflow",
        max_results=100,
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
    start_date="2024-01-01",
    end_date="2024-12-31",
    max_results=100,
)
```

### TwitterGetUserFollowersOperator
Get followers list for a user.

```python
get_followers = TwitterGetUserFollowersOperator(
    task_id="get_followers",
    username="KaitoEasyAPI",
    max_results=100,
)
```

### TwitterGetUserFollowingsOperator
Get following list for a user.

```python
get_followings = TwitterGetUserFollowingsOperator(
    task_id="get_followings",
    username="KaitoEasyAPI",
    max_results=100,
)
```

### TwitterGetUserTweetsOperator
Get tweets from a user's timeline.

```python
get_tweets = TwitterGetUserTweetsOperator(
    task_id="get_user_tweets",
    username="KaitoEasyAPI",
    max_results=50,
)
```

## Using the Hook Directly

For more complex workflows, use the `TwitterApiHook` directly:

```python
from airflow_provider_twitterapi.hooks.twitterapi import TwitterApiHook

hook = TwitterApiHook(twitterapi_conn_id="twitterapi_default")

# Get user profile
user_data = hook.get_user_by_username("KaitoEasyAPI")

# Search tweets
tweets = hook.search_tweets(
    query="python",
    start_date="2024-01-01",
    max_results=100
)
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
apache-airflow-provider-twitterapi/
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
