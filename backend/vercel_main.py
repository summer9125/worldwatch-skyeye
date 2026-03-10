"""
Vercel Serverless Function 入口
"""
import sys
import os

# 添加 backend 目录到 Python 路径
sys.path.insert(0, os.path.dirname(__file__))

# 现在可以正确导入 app 模块
from app.main import app

# Vercel 需要这个变量名
handler = app
