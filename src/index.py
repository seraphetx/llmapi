from main import app

# Cloudflare Workers入口点
async def fetch(request, env, ctx):
    """
    Cloudflare Workers fetch处理器
    """
    # 将环境绑定到FastAPI应用
    app.state.env = env
    
    # 直接使用FastAPI的ASGI接口
    return await app(request, env, ctx)