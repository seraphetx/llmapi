from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from models import ChatRequest, ChatResponse, ErrorResponse
from database import db
from llm_service import llm_service
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LLM API Service",
    description="大模型API转发服务",
    version="1.0.0"
)

@app.get("/")
async def root():
    """根路径，返回API信息"""
    return {
        "message": "LLM API Service",
        "version": "1.0.0",
        "description": "大模型API转发服务"
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    聊天接口
    
    Args:
        request: 包含token和prompt的请求体
        
    Returns:
        ChatResponse: 包含大模型返回结果的响应
        
    Raises:
        HTTPException: 当token无效时返回500错误
    """
    try:
        logger.info(f"收到聊天请求，token: {request.token[:10]}...")
        
        # 验证token并获取api_key
        api_key = db.get_api_key_by_token(request.token)
        
        if not api_key:
            logger.warning(f"无效的token: {request.token[:10]}...")
            raise HTTPException(
                status_code=500,
                detail="无效的token"
            )
        
        logger.info("Token验证成功，调用大模型API")
        
        # 调用大模型API
        result = llm_service.call_llm_api(api_key, request.prompt)
        
        if result["success"]:
            logger.info("大模型API调用成功")
            return ChatResponse(
                success=True,
                data=result["data"]
            )
        else:
            logger.error(f"大模型API调用失败: {result['error']}")
            raise HTTPException(
                status_code=500,
                detail=f"大模型API调用失败: {result['error']}"
            )
            
    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except Exception as e:
        logger.error(f"处理聊天请求时发生未知错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"服务器内部错误: {str(e)}"
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error=exc.detail).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """通用异常处理器"""
    logger.error(f"未处理的异常: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(error="服务器内部错误").dict()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)