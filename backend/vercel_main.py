"""
Vercel Serverless Function 入口
"""
from app.main import app

# Vercel 需要这个变量名
handler = app
