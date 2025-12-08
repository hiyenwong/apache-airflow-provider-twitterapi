"""测试 TwitterApiHook 的集成功能"""

import os

from airflow_provider_twitterapi.hooks.twitterapi import TwitterApiHook


# 模拟 Airflow Connection
class MockConnection:
    def __init__(self, password):
        self.password = password
        self.extra_dejson = {}


class MockHook(TwitterApiHook):
    """用于测试的 Mock Hook，不需要真实的 Airflow Connection"""

    def __init__(self, api_key):
        self.conn_id = "test"
        self.api_key = api_key
        self.log = self._get_logger()

    def _get_logger(self):
        import logging

        return logging.getLogger(__name__)

    def get_connection(self, conn_id):
        return MockConnection(self.api_key)


def test_all_endpoints():
    """测试所有 API 端点"""
    api_key = os.environ.get("TWITTER_API_KEY", "c85ad653e5c2449b9f3a4f3c52dcd79b")
    hook = MockHook(api_key)

    print("=" * 60)
    print("测试 TwitterApiHook 的所有方法")
    print("=" * 60)

    # 1. 测试获取用户信息
    print("\n1. 测试 get_user_by_username()")
    try:
        result = hook.get_user_by_username(username="elonmusk")
        user_data = result.get("data", {})
        print(
            f"✓ 成功获取用户: {user_data.get('userName')} (ID: {user_data.get('id')})"
        )
        print(f"  粉丝数: {user_data.get('friendsCount')}")
    except Exception as e:
        print(f"✗ 失败: {e}")

    # 2. 测试获取用户推文
    print("\n2. 测试 get_user_tweets()")
    try:
        result = hook.get_user_tweets(username="elonmusk")
        tweets = result.get("data", {}).get("tweets", [])
        print(f"✓ 成功获取 {len(tweets)} 条推文")
        if tweets:
            print(f"  最新推文: {tweets[0].get('text', '')[:80]}...")
    except Exception as e:
        print(f"✗ 失败: {e}")

    # 3. 测试高级搜索
    print("\n3. 测试 search_tweets()")
    try:
        result = hook.search_tweets(query="from:elonmusk", query_type="Latest")
        tweets = result.get("tweets", [])
        print(f"✓ 成功搜索到 {len(tweets)} 条推文")
    except Exception as e:
        print(f"✗ 失败: {e}")

    # 4. 测试获取粉丝
    print("\n4. 测试 get_user_followers()")
    try:
        result = hook.get_user_followers(username="elonmusk", page_size=5)
        followers = result.get("followers", [])
        print(f"✓ 成功获取 {len(followers)} 个粉丝")
        if followers:
            print(f"  示例粉丝: {followers[0].get('userName')}")
    except Exception as e:
        print(f"✗ 失败: {e}")

    # 5. 测试获取关注
    print("\n5. 测试 get_user_followings()")
    try:
        result = hook.get_user_followings(username="elonmusk", page_size=5)
        followings = result.get("followings", [])
        print(f"✓ 成功获取 {len(followings)} 个关注")
        if followings:
            print(f"  示例关注: {followings[0].get('userName')}")
    except Exception as e:
        print(f"✗ 失败: {e}")

    # 6. 测试通过 ID 获取推文
    print("\n6. 测试 get_tweet_by_ids()")
    try:
        # 先获取一些推文 ID
        result = hook.get_user_tweets(username="elonmusk")
        tweets = result.get("data", {}).get("tweets", [])
        if tweets:
            tweet_id = tweets[0].get("id")
            result = hook.get_tweet_by_ids(tweet_ids=[tweet_id])
            print(f"✓ 成功获取推文: {result.get('data', {}).get('text', '')[:80]}...")
    except Exception as e:
        print(f"✗ 失败: {e}")

    print("\n" + "=" * 60)
    print("所有测试完成!")
    print("=" * 60)


if __name__ == "__main__":
    test_all_endpoints()
