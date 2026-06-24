# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Optional Xquik backend for the existing hook and operators via
  `api_provider="xquik"` or connection extra `{"api_provider": "xquik"}`.
- Xquik endpoint mapping for tweet lookup, user lookup, tweet search,
  user tweets, followers, and following.

## [2025.12.10] - 2025-12-10

### Added
- **New Operator**: `TwitterSearchUserTweetsByDateOperator` - Search tweets from a specific user within a custom date range
- **New Hook Method**: `search_user_tweets_by_date()` - Enables searching user tweets with date filters (since/until parameters)
- Support for additional search filters (e.g., language filters, reply filters)
- Comprehensive example in `example_twitterapi_dag.py` demonstrating date range search

### Changed
- Updated README with accurate operator examples matching actual implementation
- Fixed all operator documentation to show correct parameters (removed non-existent `max_results` parameter)
- Improved documentation with better examples using real Twitter usernames

### Documentation
- Added date range search examples to README
- Updated all code examples to match actual API parameters
- Added usage examples for `search_user_tweets_by_date()` hook method
- Improved Quick Start guide with more realistic examples

## [2025.12.09.post3] - 2025-12-09

### Initial Release
- TwitterAPI.io hook with full API coverage
- Operators for tweets, users, followers, followings, and search
- Airflow 2.11+ compatibility
- Type-safe implementation with Python 3.9+
- Proper error handling and logging
