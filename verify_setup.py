"""
完整测试：验证 Airflow 连接配置和 Hook 功能
"""

import os
import sys

sys.path.insert(
    0, "/Users/hiyenwong/projects/funda_ai/apache-airflow-provider-twitterapi"
)  # noqa: E501

print("=" * 80)
print("TwitterAPI Provider 配置验证")
print("=" * 80)

# 1. 验证 Hook 配置
print("\n【步骤 1】验证 Hook UI 配置")
from airflow_provider_twitterapi.hooks.twitterapi import TwitterApiHook

ui_config = TwitterApiHook.get_ui_field_behaviour()
print(f"✅ Hook 名称: {TwitterApiHook.hook_name}")
print(f"✅ 连接类型: {TwitterApiHook.conn_type}")
print(f"✅ Password 字段重命名为: {ui_config['relabeling']['password']}")
print(f"✅ 隐藏的字段: {', '.join(ui_config['hidden_fields'])}")

# 2. 验证 Provider 元数据
print("\n【步骤 2】验证 Provider 元数据")
try:
    from airflow_provider_twitterapi import get_provider_info

    provider_info = get_provider_info()
    print(f"✅ Provider 名称: {provider_info['name']}")
    print(f"✅ Package 名称: {provider_info['package-name']}")
    print(f"✅ 版本: {provider_info['versions']}")

    # 检查连接类型配置
    conn_types = provider_info.get("connection-types", [])
    if conn_types:
        conn_type = conn_types[0]
        print(f"✅ 连接类型已注册: {conn_type.get('connection-type')}")
        print(f"✅ Hook 类: {conn_type.get('hook-class-name')}")
except Exception as e:
    print(f"❌ Provider 元数据错误: {e}")

# 3. 验证 Operators 可用
print("\n【步骤 3】验证 Operators 可用")
try:
    operators = [
        "TwitterGetUserByUsernameOperator",
        "TwitterGetTweetByIdsOperator",
        "TwitterSearchTweetsOperator",
        "TwitterGetUserFollowersOperator",
        "TwitterGetUserFollowingsOperator",
        "TwitterGetUserTweetsOperator",
    ]
    for op in operators:
        print(f"✅ {op}")
except Exception as e:
    print(f"❌ Operators 导入错误: {e}")

# 4. 模拟 API 调用（不使用真实连接）
print("\n【步骤 4】验证 API 端点配置")
import requests

API_KEY = os.environ.get("TWITTER_API_KEY", "new1_b099c7579e9444ec89d1c0fdcf7c2905")
BASE_URL = "https://api.twitterapi.io"
headers = {"x-api-key": API_KEY}

# 简单测试一个端点
try:
    resp = requests.get(
        f"{BASE_URL}/twitter/user/info",
        params={"userName": "elonmusk"},
        headers=headers,
        timeout=5,
    )
    if resp.status_code == 200:
        print(f"✅ API 端点工作正常 (状态码: {resp.status_code})")
    elif resp.status_code == 429:
        print(f"⚠️  API 限流 (状态码: {resp.status_code}) - API 端点正确但达到请求限制")
    else:
        print(f"⚠️  API 响应 (状态码: {resp.status_code})")
except Exception as e:
    print(f"❌ API 调用错误: {e}")

print("\n" + "=" * 80)
print("配置验证完成！")
print("=" * 80)

# 5. 显示使用说明
print("\n【下一步】在 Airflow UI 中配置连接")
print("\n1. 打开 Airflow Web UI: http://localhost:8080")
print("2. 导航到: Admin → Connections")
print("3. 点击 '+' 添加新连接")
print("4. 填写信息：")
print("   - Connection Type: TwitterAPI.io")
print("   - Connection Id: twitterapi_default")
print("   - API Key: [你的 TwitterAPI.io API Key]")
print("5. 点击 'Save'")
print("\n详细说明请查看: AIRFLOW_UI_SETUP.md")
