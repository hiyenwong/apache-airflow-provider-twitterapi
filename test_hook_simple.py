"""
直接测试 Hook 的 API 调用（不使用 Airflow 连接）
"""

import os
import sys

import requests

# 添加项目路径
sys.path.insert(
    0, "/Users/hiyenwong/projects/funda_ai/apache-airflow-provider-twitterapi"
)  # noqa: E501

API_KEY = os.environ.get("TWITTER_API_KEY", "c85ad653e5c2449b9f3a4f3c52dcd79b")
BASE_URL = "https://api.twitterapi.io"


def test_endpoints():
    """测试所有 API 端点"""
    headers = {"x-api-key": API_KEY}

    print("=" * 80)
    print("测试 TwitterAPI.io 所有端点")
    print("=" * 80)

    # 测试 1: 获取用户信息
    print("\n【测试 1】GET /twitter/user/info?userName=elonmusk")
    try:
        resp = requests.get(
            f"{BASE_URL}/twitter/user/info",
            params={"userName": "elonmusk"},
            headers=headers,
            timeout=30,
        )
        data = resp.json()
        user_data = data.get("data", {})
        print(f"✅ 状态: {resp.status_code}")
        print(f"   User ID: {user_data.get('id')}")
        print(f"   Name: {user_data.get('name')}")
    except Exception as e:
        print(f"❌ 失败: {e}")

    # 测试 2: 获取用户推文
    print("\n【测试 2】GET /twitter/user/last_tweets?userName=elonmusk")
    try:
        resp = requests.get(
            f"{BASE_URL}/twitter/user/last_tweets",
            params={"userName": "elonmusk"},
            headers=headers,
            timeout=30,
        )
        data = resp.json()
        tweets = data.get("data", {}).get("tweets", [])
        print(f"✅ 状态: {resp.status_code}")
        print(f"   获取到 {len(tweets)} 条推文")
        if tweets:
            print(f"   最新推文: {tweets[0].get('text', '')[:80]}...")
    except Exception as e:
        print(f"❌ 失败: {e}")

    # 测试 3: 高级搜索
    print("\n【测试 3】GET /twitter/tweet/advanced_search")
    try:
        resp = requests.get(
            f"{BASE_URL}/twitter/tweet/advanced_search",
            params={"query": "from:elonmusk", "queryType": "Latest"},
            headers=headers,
            timeout=30,
        )
        data = resp.json()
        tweets = data.get("tweets", [])
        print(f"✅ 状态: {resp.status_code}")
        print(f"   搜索到 {len(tweets)} 条推文")
    except Exception as e:
        print(f"❌ 失败: {e}")

    # 测试 4: 获取粉丝
    print("\n【测试 4】GET /twitter/user/followers?userName=elonmusk&pageSize=5")
    try:
        resp = requests.get(
            f"{BASE_URL}/twitter/user/followers",
            params={"userName": "elonmusk", "pageSize": 5},
            headers=headers,
            timeout=30,
        )
        data = resp.json()
        followers = data.get("followers", [])
        print(f"✅ 状态: {resp.status_code}")
        print(f"   获取到 {len(followers)} 个粉丝")
    except Exception as e:
        print(f"❌ 失败: {e}")

    # 测试 5: 获取关注
    print("\n【测试 5】GET /twitter/user/followings?userName=elonmusk&pageSize=5")
    try:
        resp = requests.get(
            f"{BASE_URL}/twitter/user/followings",
            params={"userName": "elonmusk", "pageSize": 5},
            headers=headers,
            timeout=30,
        )
        data = resp.json()
        followings = data.get("followings", [])
        print(f"✅ 状态: {resp.status_code}")
        print(f"   获取到 {len(followings)} 个关注")
    except Exception as e:
        print(f"❌ 失败: {e}")

    print("\n" + "=" * 80)
    print("所有端点测试完成!")
    print("=" * 80)


if __name__ == "__main__":
    test_endpoints()
