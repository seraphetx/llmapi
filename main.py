from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import requests
import json
from typing import Optional

app = FastAPI(title="大模型API代理", description="将用户请求转发到大模型API的代理服务")

# 请求模型
class ChatRequest(BaseModel):
    token: str
    prompt: str
    model: Optional[str] = "google/gemini-2.0-flash-001"

# 响应模型
class ChatResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None

async def get_api_key_by_token(token: str, env) -> Optional[str]:
    """
    通过token从Cloudflare D1数据库查询对应的API密钥
    """
    try:
        # 使用D1数据库查询
        stmt = env.qdb.prepare("SELECT api_key FROM keys WHERE token = ?")
        result = await stmt.bind(token).first()
        
        if result:
            return result.api_key
        return None
        
    except Exception as e:
        print(f"数据库查询错误: {e}")
        return None

def call_openrouter_api(api_key: str, prompt: str, model: str) -> dict:
    """
    调用OpenRouter API
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://youthyc.com",
        "X-Title": "AI API Proxy",
    }
    
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        response = requests.post(
            url=url,
            headers=headers,
            data=json.dumps(data),
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"API调用失败，状态码: {response.status_code}",
                "details": response.text
            }
    except Exception as e:
        return {
            "error": f"API调用异常: {str(e)}"
        }

@app.post("/chat", response_model=ChatResponse)
async def chat(request_data: ChatRequest, request: Request):
    """
    聊天API端点
    """
    try:
        # 从应用状态获取Cloudflare环境
        env = getattr(app.state, 'env', None)
        if not env:
            raise HTTPException(status_code=500, detail="环境配置错误")
        
        # 1. 验证token并获取API密钥
        api_key = await get_api_key_by_token(request_data.token, env)
        if not api_key:
            raise HTTPException(status_code=500, detail="无效的token")
        
        # 2. 调用大模型API
        result = call_openrouter_api(api_key, request_data.prompt, request_data.model)
        
        # 3. 检查结果
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return ChatResponse(success=True, data=result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

@app.get("/")
async def root():
    """
    根路径，返回API信息
    """
    return {
        "message": "大模型API代理服务",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat - POST请求，需要token和prompt参数"
        }
    }

@app.get("/health")
async def health_check():
    """
    健康检查端点
    """
    return {"status": "healthy", "message": "服务运行正常"}