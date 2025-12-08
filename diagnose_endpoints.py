#!/usr/bin/env python3
"""Diagnostic script to find working TwitterAPI.io endpoints."""

import time

import requests

API_KEY = "new1_b099c7579e9444ec89d1c0fdcf7c2905"
BASE_URL = "https://api.twitterapi.io"


def test_endpoint(path, params=None, method="GET"):
    """Test a specific endpoint."""
    headers = {"x-api-key": API_KEY}
    url = f"{BASE_URL}{path}"

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params, timeout=10)
        else:
            response = requests.post(url, headers=headers, json=params, timeout=10)

        return response.status_code, response.text[:200]
    except Exception as e:
        return None, str(e)


# Common TwitterAPI.io endpoint patterns from their docs
endpoints_to_test = [
    # User endpoints
    ("/user/by/username", {"username": "elonmusk"}),
    ("/twitter/user/by/username", {"username": "elonmusk"}),
    ("/v1/user", {"username": "elonmusk"}),
    ("/v2/users/by/username/elonmusk", None),
    ("/twitter/user/by/username/elonmusk", None),
    # Search endpoints
    ("/tweet/search", {"query": "python", "maxResults": 10}),
    ("/tweets/search", {"query": "python", "maxResults": 10}),
    ("/twitter/search", {"query": "python", "maxResults": 10}),
    # Tweet endpoints
    ("/tweet", {"tweetId": "1234567890"}),
    ("/tweets", {"ids": "1234567890"}),
]

print("=" * 70)
print("Testing TwitterAPI.io Endpoints")
print("=" * 70)

for path, params in endpoints_to_test:
    print(f"\nTesting: GET {path}")
    if params:
        print(f"Params: {params}")

    status, response = test_endpoint(path, params)

    if status == 200:
        print(f"✓ SUCCESS! Status: {status}")
        print(f"Response: {response}")
        break
    elif status == 429:
        print("⚠ Rate limited (429) - API key is working!")
        print("Waiting 6 seconds...")
        time.sleep(6)
    elif status == 404:
        print("✗ Not found (404)")
    else:
        print(f"Status: {status}, Response: {response}")

    # Small delay between requests
    time.sleep(1)

print("\n" + "=" * 70)
print("Endpoint Discovery Complete")
print("=" * 70)
