"""
完整测试 TwitterAPI Provider 的所有配置
"""

import os
import sys

sys.path.insert(
    0, "/Users/hiyenwong/projects/funda_ai/apache-airflow-provider-twitterapi"
)  # noqa: E501


def test_provider_info():
    """测试 Provider 元数据"""
    print("=" * 80)
    print("【测试 1】Provider 元数据")
    print("=" * 80)

    from airflow_provider_twitterapi import get_provider_info

    info = get_provider_info()

    print(f"✅ Package name: {info['package-name']}")
    print(f"✅ Provider name: {info['name']}")
    print(f"✅ Version: {info['versions']}")

    # 检查连接类型
    conn_types = info.get("connection-types", [])
    if conn_types:
        print(f"✅ Connection types registered: {len(conn_types)}")
        for ct in conn_types:
            print(f"   - Type: {ct.get('connection-type')}")
            print(f"   - Hook: {ct.get('hook-class-name')}")
    else:
        print("❌ No connection types registered!")
        return False

    return True


def test_hook_configuration():
    """测试 Hook 配置"""
    print("\n" + "=" * 80)
    print("【测试 2】Hook 配置")
    print("=" * 80)

    from airflow_provider_twitterapi.hooks.twitterapi import TwitterApiHook

    # 检查必需的类属性
    required_attrs = {
        "conn_name_attr": TwitterApiHook.conn_name_attr,
        "default_conn_name": TwitterApiHook.default_conn_name,
        "conn_type": TwitterApiHook.conn_type,
        "hook_name": TwitterApiHook.hook_name,
    }

    for attr, value in required_attrs.items():
        print(f"✅ {attr}: {value}")

    # 检查 UI 配置方法
    if hasattr(TwitterApiHook, "get_ui_field_behaviour"):
        ui_config = TwitterApiHook.get_ui_field_behaviour()
        print("✅ get_ui_field_behaviour exists")
        print(f"   - Hidden fields: {ui_config.get('hidden_fields', [])}")
        print(f"   - Relabeling: {ui_config.get('relabeling', {})}")
        print(f"   - Placeholders: {ui_config.get('placeholders', {})}")
    else:
        print("❌ get_ui_field_behaviour method not found!")
        return False

    return True


def test_operators():
    """测试 Operators 可用性"""
    print("\n" + "=" * 80)
    print("【测试 3】Operators 可用性")
    print("=" * 80)

    try:
        from airflow_provider_twitterapi.operators.twitterapi import (
            TwitterGetTweetByIdsOperator,
            TwitterGetUserByUsernameOperator,
            TwitterGetUserFollowersOperator,
            TwitterGetUserFollowingsOperator,
            TwitterGetUserTweetsOperator,
            TwitterSearchTweetsOperator,
        )

        operators = [
            TwitterGetUserByUsernameOperator,
            TwitterGetTweetByIdsOperator,
            TwitterSearchTweetsOperator,
            TwitterGetUserFollowersOperator,
            TwitterGetUserFollowingsOperator,
            TwitterGetUserTweetsOperator,
        ]

        for op in operators:
            print(f"✅ {op.__name__}")

        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_api_endpoints():
    """测试 API 端点"""
    print("\n" + "=" * 80)
    print("【测试 4】API 端点测试")
    print("=" * 80)

    import requests

    API_KEY = os.environ.get("TWITTER_API_KEY", "new1_b099c7579e9444ec89d1c0fdcf7c2905")
    BASE_URL = "https://api.twitterapi.io"
    headers = {"x-api-key": API_KEY}

    try:
        resp = requests.get(
            f"{BASE_URL}/twitter/user/info",
            params={"userName": "elonmusk"},
            headers=headers,
            timeout=5,
        )

        if resp.status_code == 200:
            data = resp.json()
            user_data = data.get("data", {})
            print("✅ API 端点正常工作")
            print(f"   - Status: {resp.status_code}")
            print(f"   - User: {user_data.get('name')} (@{user_data.get('userName')})")
            return True
        elif resp.status_code == 429:
            print("⚠️  API 限流 (429) - 端点正确但请求太频繁")
            return True
        else:
            print(f"⚠️  API 返回状态: {resp.status_code}")
            print(f"   Response: {resp.text[:200]}")
            return False

    except Exception as e:
        print(f"❌ API 调用失败: {e}")
        return False


def test_hook_api_methods():
    """测试 Hook 的 API 方法"""
    print("\n" + "=" * 80)
    print("【测试 5】Hook API 方法")
    print("=" * 80)

    from airflow_provider_twitterapi.hooks.twitterapi import TwitterApiHook

    hook = TwitterApiHook(twitterapi_conn_id="test")

    # 检查所有 API 方法存在
    api_methods = [
        "get_user_by_username",
        "get_user_by_userids",
        "get_tweet_by_ids",
        "search_tweets",
        "get_user_followers",
        "get_user_followings",
        "get_user_tweets",
    ]

    for method in api_methods:
        if hasattr(hook, method):
            print(f"✅ {method}")
        else:
            print(f"❌ {method} not found!")
            return False

    return True


def main():
    """运行所有测试"""
    print("\n" + "🚀" * 40)
    print("开始完整测试 TwitterAPI Provider")
    print("🚀" * 40 + "\n")

    results = []

    # 运行所有测试
    results.append(("Provider 元数据", test_provider_info()))
    results.append(("Hook 配置", test_hook_configuration()))
    results.append(("Operators 可用性", test_operators()))
    results.append(("API 端点", test_api_endpoints()))
    results.append(("Hook API 方法", test_hook_api_methods()))

    # 汇总结果
    print("\n" + "=" * 80)
    print("测试结果汇总")
    print("=" * 80)

    all_passed = True
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")
        if not result:
            all_passed = False

    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 所有测试通过！")
        print("=" * 80)
        print("\n【下一步】在 Airflow UI 中配置连接：")
        print("\n1. 安装 provider:")
        print("   pip install -e .")
        print("\n2. 重启 Airflow webserver:")
        print("   airflow webserver --port 8080")
        print("\n3. 在 UI 中添加连接:")
        print("   Admin → Connections → Add Connection")
        print("   - Connection Type: TwitterAPI.io")
        print("   - Connection Id: twitterapi_default")
        print("   - API Key: [你的 API Key]")
        print("\n4. 测试 DAG:")
        print("   airflow dags test example_twitterapi_provider")
    else:
        print("❌ 部分测试失败，请检查上面的错误信息")
        print("=" * 80)

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
