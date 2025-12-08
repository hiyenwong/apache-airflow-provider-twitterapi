"""
测试 Airflow 连接 UI 配置
"""

import sys

sys.path.insert(
    0, "/Users/hiyenwong/projects/funda_ai/apache-airflow-provider-twitterapi"
)  # noqa: E501

from airflow_provider_twitterapi.hooks.twitterapi import TwitterApiHook


def test_ui_field_behaviour():
    """测试 UI 字段配置"""
    print("=" * 80)
    print("测试 TwitterAPI 连接 UI 配置")
    print("=" * 80)

    # 获取 UI 字段配置
    ui_config = TwitterApiHook.get_ui_field_behaviour()

    print("\n【连接类型信息】")
    print(f"Hook 名称: {TwitterApiHook.hook_name}")
    print(f"连接类型: {TwitterApiHook.conn_type}")
    print(f"默认连接名: {TwitterApiHook.default_conn_name}")

    print("\n【UI 字段配置】")
    print(f"隐藏字段: {ui_config.get('hidden_fields', [])}")
    print(f"字段重命名: {ui_config.get('relabeling', {})}")
    print(f"占位符文本: {ui_config.get('placeholders', {})}")

    print("\n【验证结果】")
    checks = [
        (
            "✅" if "password" in ui_config.get("relabeling", {}) else "❌",
            "密码字段已重命名为 'API Key'",
        ),
        (
            "✅" if "password" in ui_config.get("placeholders", {}) else "❌",
            "密码字段有占位符提示",
        ),
        (
            "✅" if "host" in ui_config.get("hidden_fields", []) else "❌",
            "不必要的字段已隐藏",
        ),
    ]

    for status, message in checks:
        print(f"{status} {message}")

    print("\n" + "=" * 80)
    print("配置验证完成!")
    print("=" * 80)

    # 显示在 Airflow UI 中的效果
    print("\n【在 Airflow UI 中的显示效果】")
    print("连接类型: TwitterAPI.io")
    print("连接 ID: [用户输入]")
    print(f"API Key (密码): [{ui_config['placeholders']['password']}]")
    print("\n注意: host, schema, login, port, extra 字段将被隐藏")


if __name__ == "__main__":
    test_ui_field_behaviour()
