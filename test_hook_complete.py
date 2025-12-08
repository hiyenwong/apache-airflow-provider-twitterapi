"""
测试 TwitterApiHook 的所有方法
"""

import os
import sys

# 添加项目路径
sys.path.insert(
    0, "/Users/hiyenwong/projects/funda_ai/apache-airflow-provider-twitterapi"
)

from airflow_provider_twitterapi.hooks.twitterapi import TwitterApiHook


# 创建 mock connection
class MockConnection:
    def __init__(self, api_key):
        self.password = api_key
        self.extra_dejson = {}


class MockConnectionManager:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_connection(self, conn_id):
        return MockConnection(self.api_key)


# 测试
def test_all_endpoints():
    api_key = os.environ.get("TWITTER_API_KEY", "c85ad653e5c2449b9f3a4f3c52dcd79b")

    # 创建 hook (不需要真实的 Airflow 连接)
    hook = TwitterApiHook(twitterapi_conn_id="test")
    hook.api_key = api_key

    print("=" * 80)
    print("测试 TwitterApiHook 所有方法")
    print("=" * 80)

    # 测试 1: 获取用户信息
    print("\n【测试 1】get_user_by_username(username='elonmusk')")
    try:
        result = hook.get_user_by_username(username="elonmusk")
        user_data = result.get("data", {})
        user_id = user_data.get("id")
        name = user_data.get("name")
        print(f"✅ 成功 - User ID: {user_id}, Name: {name}")
    except Exception as e:
        print(f"❌ 失败: {e}")

    # 测试 2: 获取用户推文
    print("\n【测试 2】get_user_tweets(username='elonmusk')")
    try:
        result = hook.get_user_tweets(username="elonmusk")
        tweets = result.get("data", {}).get("tweets", [])
        print(f"✅ 成功 - 获取到 {len(tweets)} 条推文")
        if tweets:
            tweet_text = tweets[0].get("text", "")[:80]
            print(f"   最新推文: {tweet_text}...")
    except Exception as e:
        print(f"❌ 失败: {e}")

    # 测试 3: 高级搜索
    print("\n【测试 3】search_tweets(query='from:elonmusk', query_type='Latest')")
    try:
        result = hook.search_tweets(query="from:elonmusk", query_type="Latest")
        tweets = result.get("tweets", [])
        print(f"✅ 成功 - 搜索到 {len(tweets)} 条推文")
    except Exception as e:
        print(f"❌ 失败: {e}")

    # 测试 4: 获取粉丝
    print("\n【测试 4】get_user_followers(username='elonmusk', page_size=5)")
    try:
        result = hook.get_user_followers(username="elonmusk", page_size=5)
        followers = result.get("followers", [])
        print(f"✅ 成功 - 获取到 {len(followers)} 个粉丝")
    except Exception as e:
        print(f"❌ 失败: {e}")

    # 测试 5: 获取关注
    print("\n【测试 5】get_user_followings(username='elonmusk', page_size=5)")
    try:
        result = hook.get_user_followings(username="elonmusk", page_size=5)
        followings = result.get("followings", [])
        print(f"✅ 成功 - 获取到 {len(followings)} 个关注")
    except Exception as e:
        print(f"❌ 失败: {e}")

    # 测试 6: 批量获取用户信息
    print("\n【测试 6】get_user_by_userids(user_ids=['44196397'])")
    try:
        result = hook.get_user_by_userids(user_ids=["44196397"])
        print(f"✅ 成功 - {result.get('message', 'OK')}")
    except Exception as e:
        print(f"❌ 失败: {e}")

    # 测试 7: 获取推文详情
    print("\n【测试 7】get_tweet_by_ids(tweet_ids=['1234567890'])")
    try:
        result = hook.get_tweet_by_ids(tweet_ids=["1234567890"])
        print(f"✅ 成功 - {result.get('message', 'OK')}")
    except Exception as e:
        print(f"❌ 失败: {e}")

    print("\n" + "=" * 80)
    print("测试完成!")
    print("=" * 80)


if __name__ == "__main__":
    test_all_endpoints()
