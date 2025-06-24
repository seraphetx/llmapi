# 大模型API代理服务

这是一个基于Cloudflare Workers和FastAPI的大模型API代理服务，用于将用户请求转发到OpenRouter API。

## 功能特性

- 🔐 基于token的身份验证
- 🗄️ 使用Cloudflare D1数据库存储API密钥
- 🚀 支持多种大模型（通过OpenRouter）
- ⚡ 基于Cloudflare Workers的高性能部署
- 📝 FastAPI提供标准REST API接口
- 🌐 完整的CORS支持

## 项目结构

```
├── src/
│   └── index.py          # Cloudflare Workers入口文件
├── main.py               # FastAPI应用主文件
├── schema.sql            # D1数据库初始化脚本
├── wrangler.toml         # Cloudflare Workers配置文件
├── requirements.txt      # Python依赖包列表
├── deploy.sh            # 自动化部署脚本
├── test_deployed_api.py # API测试脚本
├── README.md            # 项目文档
└── ai.md                # 原始需求文档
```

## 技术架构

- **FastAPI** - 提供标准的REST API接口
- **Cloudflare Workers** - 无服务器运行环境
- **Cloudflare D1** - SQLite兼容的边缘数据库
- **OpenRouter** - 大模型API聚合服务

## 部署步骤

### 1. 环境准备

```bash
# 安装Wrangler CLI
npm install -g wrangler

# 登录Cloudflare
wrangler login
```

### 2. 创建D1数据库

```bash
# 创建数据库
wrangler d1 create qdb

# 记录返回的database_id，更新wrangler.toml中的database_id
```

### 3. 初始化数据库

```bash
# 执行SQL脚本创建表结构和示例数据
wrangler d1 execute qdb --file=./schema.sql
```

### 4. 配置项目

编辑 `wrangler.toml` 文件：
- 将 `database_id` 替换为步骤2中获得的实际ID
- 更新 `SITE_URL` 和 `SITE_NAME` 变量（可选）

### 5. 部署

```bash
# 使用部署脚本（推荐）
chmod +x deploy.sh
./deploy.sh

# 或者直接部署
wrangler deploy
```

## API使用说明

### 基础信息

- **基础URL**: `https://your-worker.your-subdomain.workers.dev`
- **Content-Type**: `application/json`

### API端点

#### 1. 根路径 - 获取API信息

```http
GET /
```

**响应示例：**
```json
{
  "message": "大模型API代理服务",
  "version": "1.0.0",
  "endpoints": {
    "chat": "/chat - POST请求，需要token和prompt参数"
  }
}
```

#### 2. 健康检查

```http
GET /health
```

**响应示例：**
```json
{
  "status": "healthy",
  "message": "服务运行正常"
}
```

#### 3. 聊天API

```http
POST /chat
```

**请求参数：**
```json
{
  "token": "your_token_here",
  "prompt": "你好，请介绍一下你自己",
  "model": "google/gemini-2.0-flash-001"  // 可选，默认为gemini-2.0-flash-001
}
```

**成功响应：**
```json
{
  "success": true,
  "data": {
    "id": "chatcmpl-...",
    "object": "chat.completion",
    "created": 1234567890,
    "model": "google/gemini-2.0-flash-001",
    "choices": [
      {
        "index": 0,
        "message": {
          "role": "assistant",
          "content": "你好！我是一个AI助手..."
        },
        "finish_reason": "stop"
      }
    ],
    "usage": {
      "prompt_tokens": 10,
      "completion_tokens": 20,
      "total_tokens": 30
    }
  }
}
```

**错误响应：**
```json
{
  "success": false,
  "error": "无效的token"
}
```

## 数据库管理

### 查看所有API密钥

```bash
wrangler d1 execute qdb --command="SELECT id, name, token, provider, created_at FROM keys"
```

### 添加新的API密钥

```bash
wrangler d1 execute qdb --command="INSERT INTO keys (name, token, api_key, provider) VALUES ('用户名', 'user_token_123', 'sk-or-v1-...', 'openrouter')"
```

### 更新API密钥

```bash
wrangler d1 execute qdb --command="UPDATE keys SET api_key = 'new_api_key' WHERE token = 'user_token'"
```

### 删除API密钥

```bash
wrangler d1 execute qdb --command="DELETE FROM keys WHERE token = 'token_to_delete'"
```

## 支持的模型

通过OpenRouter API，支持以下模型：

### 推荐模型
- `google/gemini-2.0-flash-001` - Google最新模型，速度快
- `anthropic/claude-3-5-sonnet` - Anthropic高质量模型
- `openai/gpt-4o` - OpenAI最新模型
- `openai/gpt-4o-mini` - OpenAI经济型模型

### 更多模型
完整模型列表请参考 [OpenRouter文档](https://openrouter.ai/docs#models)

## 测试

### 本地测试

使用提供的测试脚本：

```bash
# 更新test_deployed_api.py中的BASE_URL
python test_deployed_api.py
```

### 使用curl测试

```bash
# 健康检查
curl https://your-worker.your-subdomain.workers.dev/health

# 聊天API测试
curl -X POST https://your-worker.your-subdomain.workers.dev/chat \
  -H "Content-Type: application/json" \
  -d '{
    "token": "test_token_123",
    "prompt": "你好",
    "model": "google/gemini-2.0-flash-001"
  }'
```

## 监控和调试

### 查看实时日志

```bash
wrangler tail
```

### 查看部署状态

```bash
wrangler deployments list
```

### 查看Workers使用情况

```bash
wrangler analytics
```

## 安全注意事项

1. **保护API密钥**
   - 确保OpenRouter API密钥安全存储在D1数据库中
   - 定期轮换API密钥

2. **Token管理**
   - 为每个用户生成唯一的token
   - 定期检查和清理无效token

3. **访问控制**
   - 考虑添加IP白名单
   - 实施请求频率限制
   - 监控异常使用模式

4. **数据保护**
   - 不要在日志中记录敏感信息
   - 定期备份D1数据库

## 故障排除

### 常见错误

1. **"无效的token"**
   - 检查token是否在数据库中存在
   - 确认token拼写正确

2. **"D1数据库未正确绑定"**
   - 确认wrangler.toml中的database_id正确
   - 检查数据库是否已创建

3. **"API调用失败"**
   - 检查OpenRouter API密钥是否有效
   - 确认API密钥有足够的额度
   - 检查网络连接

4. **部署失败**
   - 确认已登录Cloudflare
   - 检查wrangler.toml配置
   - 查看详细错误信息

### 调试技巧

```bash
# 查看详细日志
wrangler tail --format=pretty

# 检查Workers状态
wrangler status

# 验证数据库连接
wrangler d1 execute qdb --command="SELECT COUNT(*) FROM keys"
```

## 性能优化

1. **缓存策略**
   - 考虑缓存频繁查询的token验证结果
   - 使用Cloudflare KV存储临时数据

2. **请求优化**
   - 实施请求去重
   - 添加请求超时控制

3. **监控指标**
   - 监控响应时间
   - 跟踪错误率
   - 分析使用模式

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 支持

如果遇到问题，请：
1. 查看故障排除部分
2. 检查Cloudflare Workers文档
3. 提交Issue描述问题
