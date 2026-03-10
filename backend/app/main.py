"""
FastAPI 应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.config import settings
from app.api import events, intelligence, reports

app = FastAPI(
    title="WorldWatch 天眼",
    description="全球情报监控系统",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "ok", "system": "WorldWatch", "version": "1.0.0"}

# 首页
@app.get("/")
async def index():
    static_path = os.path.join(os.path.dirname(__file__), "static")
    return FileResponse(os.path.join(static_path, "index.html"))

# 注册路由
app.include_router(events.router, prefix="/api/v1/events", tags=["事件管理"])
app.include_router(intelligence.router, prefix="/api/v1/intelligence", tags=["情报分析"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["情报简报"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
