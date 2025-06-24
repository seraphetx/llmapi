#!/bin/bash

echo "🚀 开始部署大模型API代理服务到Cloudflare Workers"
echo "================================================"

# 检查是否安装了wrangler
if ! command -v wrangler &> /dev/null; then
    echo "❌ 错误: 未找到wrangler CLI"
    echo "请先安装: npm install -g wrangler"
    exit 1
fi

# 检查是否已登录
echo "📋 检查登录状态..."
if ! wrangler whoami &> /dev/null; then
    echo "❌ 未登录Cloudflare"
    echo "请先登录: wrangler login"
    exit 1
fi

echo "✅ 已登录Cloudflare"

# 检查wrangler.toml配置
if [ ! -f "wrangler.toml" ]; then
    echo "❌ 错误: 未找到wrangler.toml配置文件"
    exit 1
fi

# 检查是否已配置数据库ID
if grep -q "your-d1-database-id" wrangler.toml; then
    echo "⚠️  警告: 请先在wrangler.toml中配置正确的database_id"
    echo "使用以下命令创建数据库: wrangler d1 create qdb"
    read -p "是否已经配置了正确的database_id? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "请先配置database_id后再运行此脚本"
        exit 1
    fi
fi

# 初始化数据库（如果需要）
echo "🗄️  初始化数据库..."
if [ -f "schema.sql" ]; then
    echo "执行数据库初始化脚本..."
    wrangler d1 execute qdb --file=./schema.sql
    if [ $? -eq 0 ]; then
        echo "✅ 数据库初始化成功"
    else
        echo "⚠️  数据库初始化可能失败，请检查是否已经初始化过"
    fi
else
    echo "⚠️  未找到schema.sql文件"
fi

# 部署到Cloudflare Workers
echo "🚀 部署到Cloudflare Workers..."
wrangler deploy

if [ $? -eq 0 ]; then
    echo "✅ 部署成功!"
    echo ""
    echo "🎉 部署完成!"
    echo "================================================"
    echo "您的API现在可以通过以下URL访问:"
    echo "https://your-worker.your-subdomain.workers.dev"
    echo ""
    echo "📚 API端点:"
    echo "- GET  /health - 健康检查"
    echo "- GET  / - API信息"
    echo "- POST /chat - 聊天API"
    echo ""
    echo "📝 下一步:"
    echo "1. 在D1数据库中添加有效的API密钥"
    echo "2. 使用test_deployed_api.py测试API"
    echo "3. 查看日志: wrangler tail"
else
    echo "❌ 部署失败"
    exit 1
fi