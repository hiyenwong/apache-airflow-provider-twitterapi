# 在 Airflow UI 中配置 TwitterAPI 连接 - 完整指南

## ✅ Provider 已安装成功

```
Package: apache-airflow-provider-twitterapi
Version: 0.1.2
Connection Type: twitterapi
```

---

## 📋 在 Airflow UI 中添加连接

### 步骤 1: 启动 Airflow Webserver

```bash
# 在 airflow2 环境中启动
conda activate airflow2
airflow webserver --port 8080
```

在另一个终端启动 scheduler：
```bash
conda activate airflow2
airflow scheduler
```

### 步骤 2: 访问 Airflow UI

在浏览器中打开：
```
http://localhost:8080
```

使用你的 Airflow 账号登录（默认是 admin/admin）

### 步骤 3: 添加新连接

1. 点击顶部菜单 **Admin** → **Connections**

2. 点击右上角的 **+** 按钮（Add a new record）

3. 填写连接信息：

   ```
   ┌─────────────────────────────────────────────────────┐
   │ Connection Id *                                     │
   │ ┌─────────────────────────────────────────────────┐ │
   │ │ twitterapi_default                              │ │
   │ └─────────────────────────────────────────────────┘ │
   │                                                     │
   │ Connection Type *                                   │
   │ ┌─────────────────────────────────────────────────┐ │
   │ │ TwitterAPI.io                           ▼       │ │
   │ └─────────────────────────────────────────────────┘ │
   │                                                     │
   │ API Key                                             │
   │ ┌─────────────────────────────────────────────────┐ │
   │ │ new1_b099c7579e9444ec89d1c0fdcf7c2905          │ │
   │ └─────────────────────────────────────────────────┘ │
   │                                                     │
   │ [ Test ]  [ Save ]  [ Cancel ]                     │
   └─────────────────────────────────────────────────────┘
   ```

   **字段说明：**
   
   - **Connection Id**: `twitterapi_default` 
     - 这是在 DAG 中引用连接的名称
     - 可以自定义，但 `twitterapi_default` 是默认值
   
   - **Connection Type**: 选择 `TwitterAPI.io`
     - 下拉菜单中查找 "TwitterAPI.io" 或 "twitterapi"
     - 如果看不到，说明 provider 未正确安装
   
   - **API Key**: 输入你的 TwitterAPI.io API Key
     - 格式通常是 `new1_xxxxxxxxxxxxx`
     - 从 https://twitterapi.io/dashboard 获取

4. 点击 **Save** 保存

### 步骤 4: 验证连接

点击连接列表中的 **Test** 按钮（如果可用）

---

## 🎯 在 DAG 中使用连接

创建一个测试 DAG：

```python
from datetime import datetime
from airflow import DAG
from airflow_provider_twitterapi.operators.twitterapi import (
    TwitterGetUserTweetsOperator
)

with DAG(
    'test_twitterapi',
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    
    # 使用默认连接 ID
    get_tweets = TwitterGetUserTweetsOperator(
        task_id='get_elon_tweets',
        username='elonmusk',
        # twitterapi_conn_id='twitterapi_default',  # 可选，这是默认值
    )
    
    # 或使用自定义连接 ID
    get_tweets_custom = TwitterGetUserTweetsOperator(
        task_id='get_tweets_with_custom_conn',
        username='elonmusk',
        twitterapi_conn_id='my_twitter_connection',  # 使用自定义的连接 ID
    )
```

---

## 🔍 故障排查

### 问题 1: Connection Type 下拉菜单中看不到 "TwitterAPI.io"

**解决方案：**

1. 确认 provider 已安装：
   ```bash
   conda activate airflow2
   pip list | grep twitterapi
   ```
   
   应该看到：
   ```
   apache-airflow-provider-twitterapi  0.1.2
   ```

2. 重启 Airflow webserver：
   ```bash
   # 停止当前的 webserver (Ctrl+C)
   # 然后重新启动
   conda activate airflow2
   airflow webserver --port 8080
   ```

3. 验证 provider 已注册：
   ```bash
   conda activate airflow2
   airflow providers list | grep -i twitter
   ```

### 问题 2: 连接测试失败

**可能原因：**

1. **API Key 无效或过期**
   - 检查 API Key 格式是否正确
   - 前往 https://twitterapi.io/dashboard 验证 API Key

2. **API 配额不足**
   - 错误信息：`Credits is not enough. Please recharge`
   - 需要在 TwitterAPI.io 充值

3. **API 限流**
   - 错误信息：`429 Too Many Requests`
   - 等待一段时间后重试

### 问题 3: 保存连接后显示为空

**解决方案：**
- 确保 Airflow 数据库已初始化：
  ```bash
  airflow db init
  ```

---

## 📝 使用 CLI 添加连接（替代方法）

如果 UI 不可用，可以使用命令行：

```bash
# 方法 1: 使用参数
conda activate airflow2
airflow connections add twitterapi_default \
    --conn-type twitterapi \
    --conn-password "new1_b099c7579e9444ec89d1c0fdcf7c2905"

# 方法 2: 使用 URI
airflow connections add twitterapi_default \
    --conn-uri "twitterapi://:new1_b099c7579e9444ec89d1c0fdcf7c2905@"

# 验证连接已创建
airflow connections get twitterapi_default
```

---

## ✅ 配置完成检查清单

- [ ] Provider 已安装 (版本 0.1.2)
- [ ] Airflow webserver 已启动
- [ ] 在 UI 中能看到 "TwitterAPI.io" 连接类型
- [ ] 连接已保存，Connection Id 为 `twitterapi_default`
- [ ] API Key 已正确填写
- [ ] 可以在 DAG 中使用 TwitterAPI operators

---

## 🎉 下一步

现在你可以：

1. 查看示例 DAG：
   ```bash
   cat examples/example_twitterapi_dag.py
   ```

2. 运行测试 DAG：
   ```bash
   airflow dags test test_twitterapi
   ```

3. 开始构建你的 Twitter 数据管道！

---

## 📚 相关文档

- Provider 源码：https://github.com/hiyenwong/apache-airflow-provider-twitterapi
- TwitterAPI.io 文档：https://docs.twitterapi.io/
- Airflow 连接文档：https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html
