# 在 Airflow UI 中配置 TwitterAPI 连接

## 配置步骤

### 1. 安装 Provider

```bash
pip install -e .
```

### 2. 在 Airflow UI 中添加连接

1. 打开 Airflow Web UI
2. 导航到 **Admin** → **Connections**
3. 点击 **+** 按钮添加新连接

### 3. 填写连接信息

在连接配置页面，你会看到以下字段：

- **Connection Id**: 输入连接标识符，例如 `twitterapi_default`
- **Connection Type**: 从下拉菜单选择 **TwitterAPI.io**
- **API Key** (密码字段): 输入你的 TwitterAPI.io 或 Xquik API Key
  - 示例: `YOUR_API_KEY`
  - 获取地址: https://twitterapi.io/dashboard
- **Extra** (可选): 如果使用 Xquik，填写 `{"api_provider": "xquik"}`

**注意**: Host、Schema、Login、Port 已被自动隐藏，因为不需要配置。Extra 仅在切换 provider 时使用。

### 4. 测试连接

保存后，你可以在 DAG 中使用这个连接：

```python
from airflow_provider_twitterapi.operators.twitterapi import TwitterGetUserTweetsOperator

# 使用默认连接 ID
get_tweets = TwitterGetUserTweetsOperator(
    task_id='get_user_tweets',
    username='elonmusk',
    twitterapi_conn_id='twitterapi_default',  # 可选，默认值
)

# 或使用自定义连接 ID
get_tweets = TwitterGetUserTweetsOperator(
    task_id='get_user_tweets',
    username='elonmusk',
    twitterapi_conn_id='my_twitter_conn',  # 你创建的连接 ID
)
```

## UI 显示效果

配置后，连接表单将显示：

```
┌─────────────────────────────────────────────┐
│ Connection Type: TwitterAPI.io              │
│ Connection Id: twitterapi_default           │
│ API Key: *********************************** │
│                                             │
│ [ Test ]  [ Save ]  [ Cancel ]             │
└─────────────────────────────────────────────┘
```

## 使用命令行配置（可选）

你也可以使用 Airflow CLI 创建连接：

```bash
# 方式 1: 使用 password 参数
airflow connections add twitterapi_default \
    --conn-type twitterapi \
    --conn-password "YOUR_API_KEY"

# 使用 Xquik backend
airflow connections add xquik_default \
    --conn-type twitterapi \
    --conn-password "YOUR_XQUIK_API_KEY" \
    --conn-extra '{"api_provider": "xquik"}'

# 方式 2: 使用 URI
airflow connections add twitterapi_default \
    --conn-uri "twitterapi://:YOUR_API_KEY@"
```

## 获取 API Key

1. 访问 https://twitterapi.io 或 https://dashboard.xquik.com
2. 注册账号
3. 复制你的 API Key

## 故障排查

### 连接类型未显示

如果在下拉菜单中看不到 "TwitterAPI.io"：

1. 确认 provider 已正确安装：
   ```bash
   pip list | grep apache-airflow-provider-twitterapi
   ```

2. 重启 Airflow webserver：
   ```bash
   airflow webserver --daemon
   ```

3. 检查 provider 是否被识别：
   ```bash
   airflow providers list
   ```

### API Key 验证失败

如果连接测试失败：

1. 确认 API Key 格式正确（通常以 `new1_` 开头）
2. 检查 API Key 是否过期
3. 在 https://twitterapi.io/dashboard 验证 API Key 状态
