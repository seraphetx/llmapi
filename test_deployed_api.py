import requests
import json

# 替换为您的Cloudflare Workers URL
BASE_URL = "https://your-worker.your-subdomain.workers.dev"

def test_health_check():
    """
    测试健康检查端点
    """
    print("测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"请求失败: {e}")
    print("-" * 50)

def test_root_endpoint():
    """
    测试根端点
    """
    print("测试根端点...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"请求失败: {e}")
    print("-" * 50)

def test_chat_api():
    """
    测试聊天API
    """
    print("测试聊天API...")
    
    # 测试数据 - 请替换为您数据库中的实际token
    test_data = {
        "token": "test_token_123",
        "prompt": "你好，请介绍一下你自己。",
        "model": "google/gemini-2.0-flash-001"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            headers=headers,
            data=json.dumps(test_data),
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
    
    print("-" * 50)

def test_invalid_token():
    """
    测试无效token
    """
    print("测试无效token...")
    
    test_data = {
        "token": "invalid_token",
        "prompt": "测试无效token",
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            headers=headers,
            data=json.dumps(test_data)
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
    
    print("-" * 50)

if __name__ == "__main__":
    print("开始API测试...")
    print("=" * 50)
    print(f"测试URL: {BASE_URL}")
    print("请确保已经:")
    print("1. 部署了Cloudflare Workers")
    print("2. 创建并初始化了D1数据库")
    print("3. 在数据库中添加了有效的API密钥")
    print("4. 更新了BASE_URL为您的实际Workers URL")
    print("=" * 50)
    
    test_health_check()
    test_root_endpoint()
    test_chat_api()
    test_invalid_token()
    
    print("测试完成!")
    print("\n注意事项:")
    print("- 如果聊天API测试失败，请检查数据库中是否有对应的token")
    print("- 请确保OpenRouter API密钥有效且有足够的额度")
    print("- 可以通过Wrangler查看详细日志: wrangler tail")