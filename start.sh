#!/bin/bash
# WorldWatch 天眼 - 启动脚本

cd "$(dirname "$0")/backend"

echo "🌍 启动 WorldWatch 天眼系统..."
echo ""

# 安装依赖
echo "📦 检查依赖..."
pip3 install -r requirements.txt -q

# 初始化数据库
echo "🗄️ 初始化数据库..."
python3 -c "
from app.database import engine, Base
from app.models import Event, Intelligence, Alert
Base.metadata.create_all(bind=engine)
print('✅ 数据库初始化完成')
"

# 启动服务
echo "🚀 启动服务..."
echo "   访问地址：http://localhost:8001"
echo ""

python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
