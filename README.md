# LLM API 转发服务

这是一个基于FastAPI的大模型API转发服务，用于将用户请求转发到OpenRouter API。

## 功能特性

- 基于token的身份验证
- 支持转发用户请求到大模型API
- 使用SQLite数据库存储用户token和API密钥
- 完整的错误处理和日志记录

## 项目结构

```
.
├── main.py           # FastAPI主应用
├── database.py       # 数据库操作
├── models.py         # Pydantic数据模型
├── llm_service.py    # 大模型API调用服务
├── init_db.py        # 数据库初始化脚本
├── requirements.txt  # 项目依赖
├── README.md         # 项目说明
└── qdb.db           # SQLite数据库文件（运行后生成）
```

## 安装和运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 初始化数据库：
```bash
python init_db.py
```

3. 启动服务：
```bash
python main.py
```

或者使用uvicorn：
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API接口

### 1. 聊天接口

**POST** `/chat`

请求体：
```json
{
  "token": "your_token_here",
  "prompt": "你好，请介绍一下自己"
}
```

响应：
```json
{
  "success": true,
  "data": {
    "id": "chatcmpl-xxx",
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
    ]
  }
}
```

### 2. 健康检查

**GET** `/health`

响应：
```json
{
  "status": "healthy"
}
```

### 3. 根路径

**GET** `/`

响应：
```json
{
  "message": "LLM API Service",
  "version": "1.0.0",
  "description": "大模型API转发服务"
}
```

## 数据库结构

### keys表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| name | TEXT | 用户名称 |
| token | TEXT | 用户token（唯一） |
| api_key | TEXT | OpenRouter API密钥 |
| provider | TEXT | 服务提供商 |
| created_at | DATETIME | 创建时间，默认当前时间 |
| updated_at | DATETIME | 更新时间，自动更新 |

## 配置说明

1. 在使用前，需要在数据库中添加有效的OpenRouter API密钥
2. 可以修改 `init_db.py` 中的示例数据，添加真实的API密钥
3. 默认使用的模型是 `google/gemini-2.0-flash-001`，可在 `llm_service.py` 中修改

## 错误处理

- 当token不存在时，返回500错误
- 当API调用失败时，返回500错误并包含详细错误信息
- 所有错误都会记录到日志中

## 注意事项

1. 请确保OpenRouter API密钥的有效性
2. 建议在生产环境中使用环境变量来管理敏感信息
3. 可以根据需要调整日志级别和输出格式