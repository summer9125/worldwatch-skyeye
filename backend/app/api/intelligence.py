"""
情报分析 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db

router = APIRouter()


@router.get("/hot", summary="热门情报")
async def get_hot_intelligence(limit: int = 20, db: Session = Depends(get_db)):
    """获取热门情报"""
    return {
        "code": 0,
        "data": [
            {"id": 1, "title": "全球科技巨头发布新一代 AI 芯片", "region": "北美", "severity": "medium", "heat_score": 85.5},
            {"id": 2, "title": "某国央行宣布加息 50 个基点", "region": "欧洲", "severity": "high", "heat_score": 92.3},
            {"id": 3, "title": "国际空间站发现新型外星微生物", "region": "其他", "severity": "critical", "heat_score": 98.7}
        ]
    }


@router.get("/analysis", summary="情报分析")
async def get_analysis(db: Session = Depends(get_db)):
    """获取情报分析"""
    return {
        "code": 0,
        "data": {
            "trending_regions": ["亚洲", "欧洲", "北美"],
            "trending_categories": ["科技", "经济", "环境"],
            "risk_level": "medium"
        }
    }
