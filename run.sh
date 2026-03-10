#!/bin/bash
# WorldWatch 天眼 - 完整启动脚本

cd "$(dirname "$0")"

echo "🌍 启动 WorldWatch 天眼系统..."
echo ""

# 启动后端
echo "🚀 启动后端服务..."
cd backend
nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8001 > /tmp/worldwatch-backend.log 2>&1 &
BACKEND_PID=$!
echo "   后端 PID: $BACKEND_PID"
echo "   API 地址：http://localhost:8001"
cd ..

# 启动前端静态文件服务
echo "🌐 启动前端服务..."
cd frontend
nohup python3 -m http.server 3000 > /tmp/worldwatch-frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   前端 PID: $FRONTEND_PID"
echo "   访问地址：http://localhost:3000"
cd ..

echo ""
echo "✅ WorldWatch 天眼系统启动完成！"
echo ""
echo "📊 访问方式:"
echo "   - 前端界面：http://localhost:3000"
echo "   - API 服务：http://localhost:8001"
echo "   - API 文档：http://localhost:8001/docs"
echo ""
echo "📝 日志文件:"
echo "   - 后端：/tmp/worldwatch-backend.log"
echo "   - 前端：/tmp/worldwatch-frontend.log"
echo ""
