"""
情报简报 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import Event

router = APIRouter()


@router.get("/daily", summary="每日简报")
async def get_daily_report(db: Session = Depends(get_db)):
    """获取每日简报"""
    today = datetime.utcnow().date()
    
    return {
        "code": 0,
        "data": {
            "date": today.isoformat(),
            "summary": f"今日共监控到全球事件若干，重点关注地区为亚洲、欧洲。",
            "top_events": [],
            "risk_assessment": "中等风险"
        }
    }
