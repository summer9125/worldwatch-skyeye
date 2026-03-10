#!/bin/bash
# WorldWatch 天眼 - 一键部署到 Vercel
# 使用方法：./deploy.sh

set -e

echo "🚀 WorldWatch 天眼 - 一键部署脚本"
echo ""

# 检查 Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "📦 安装 Vercel CLI..."
    npm install -g vercel
fi

cd "$(dirname "$0")/backend"

echo ""
echo "🔐 登录 Vercel..."
echo "   请在浏览器中完成登录"
vercel login

echo ""
echo "🚀 开始部署..."
DEPLOY_URL=$(vercel --prod 2>&1 | grep -o 'https://[^[:space:]]*.vercel.app' | head -1)

echo ""
echo "✅ 部署完成！"
echo ""
echo "🌐 访问地址：$DEPLOY_URL"
echo ""
echo "📊 API 测试："
echo "   - 健康检查：$DEPLOY_URL/health"
echo "   - 事件列表：$DEPLOY_URL/api/v1/events/list"
echo "   - 统计概览：$DEPLOY_URL/api/v1/events/stats/overview"
echo ""
