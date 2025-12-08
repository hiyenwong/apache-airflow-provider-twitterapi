#!/bin/bash
# 安装和验证 TwitterAPI Provider

set -e

echo "========================================================================"
echo "安装 TwitterAPI Provider"
echo "========================================================================"

# 1. 卸载旧版本
echo "📦 卸载旧版本..."
pip uninstall -y apache-airflow-provider-twitterapi 2>/dev/null || true

# 2. 安装当前版本
echo "📦 安装当前版本..."
pip install -e .

# 3. 验证安装
echo ""
echo "========================================================================"
echo "验证安装"
echo "========================================================================"

python -c "
from airflow_provider_twitterapi import get_provider_info
from airflow_provider_twitterapi.hooks.twitterapi import TwitterApiHook

info = get_provider_info()
print('✅ Provider 已安装')
print(f'   - Package: {info[\"package-name\"]}')
print(f'   - Version: {info[\"versions\"]}')
print(f'   - Connection Type: {info[\"connection-types\"][0][\"connection-type\"]}')

ui_config = TwitterApiHook.get_ui_field_behaviour()
print('✅ Hook 配置正确')
print(f'   - Hook Name: {TwitterApiHook.hook_name}')
print(f'   - Connection Type: {TwitterApiHook.conn_type}')
print(f'   - API Key 字段已配置')
"

echo ""
echo "========================================================================"
echo "✅ 安装完成！"
echo "========================================================================"
echo ""
echo "下一步："
echo "1. 重启 Airflow webserver:"
echo "   airflow webserver --port 8080"
echo ""
echo "2. 在 Airflow UI 中添加连接:"
echo "   Admin → Connections → + (添加)"
echo "   - Connection Type: TwitterAPI.io"
echo "   - Connection Id: twitterapi_default"
echo "   - API Key: [你的 API Key]"
echo ""
echo "3. 测试连接:"
echo "   在 DAG 中使用 TwitterGetUserTweetsOperator"
echo ""
