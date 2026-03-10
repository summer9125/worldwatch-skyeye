"""
事件管理 API
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import random

from app.database import get_db
from app.models import Event

router = APIRouter()

# 模拟数据生成
def generate_mock_events():
    """生成模拟事件数据"""
    regions = ["亚洲", "欧洲", "北美", "中东", "非洲", "南美", "大洋洲"]
    categories = ["政治", "经济", "科技", "社会", "环境", "军事"]
    severities = ["low", "medium", "high", "critical"]
    
    base_events = [
        {
            "title": "全球科技巨头发布新一代 AI 芯片，性能提升 300%",
            "region": "北美",
            "category": "科技",
            "severity": "medium",
            "summary": "多家科技巨头今日同时发布新一代 AI 芯片，采用 3nm 工艺，性能较上一代提升 300%，将深刻影响全球 AI 产业格局。",
            "heat_score": 85.5
        },
        {
            "title": "某国央行宣布加息 50 个基点，全球金融市场震荡",
            "region": "欧洲",
            "category": "经济",
            "severity": "high",
            "summary": "为应对持续高通胀，该国央行宣布加息 50 个基点，超出市场预期，导致全球股市大幅波动。",
            "heat_score": 92.3
        },
        {
            "title": "国际空间站发现新型外星微生物迹象",
            "region": "其他",
            "category": "科技",
            "severity": "critical",
            "summary": "国际空间站科研团队宣布在采集的太空样本中发现疑似外星微生物痕迹，正在进一步验证中。",
            "heat_score": 98.7
        },
        {
            "title": "东南亚多国遭遇罕见洪灾，数百万人受影响",
            "region": "亚洲",
            "category": "环境",
            "severity": "high",
            "summary": "受季风影响，东南亚多国遭遇 50 年一遇洪灾，数百万人流离失所，国际社会展开紧急救援。",
            "heat_score": 88.2
        },
        {
            "title": "全球首款量子计算机商用化，算力突破新纪录",
            "region": "亚洲",
            "category": "科技",
            "severity": "medium",
            "summary": "科技公司宣布全球首款商用量子计算机正式交付，算力达到 1000 量子比特，标志着量子计算新时代到来。",
            "heat_score": 79.4
        }
    ]
    
    events = []
    for i, base in enumerate(base_events):
        event = {
            "id": i + 1,
            "title": base["title"],
            "region": base["region"],
            "country": "",
            "category": base["category"],
            "severity": base["severity"],
            "summary": base["summary"],
            "content": base["summary"] * 3,
            "source_url": "https://example.com",
            "source": "web",
            "publish_time": (datetime.utcnow() - timedelta(hours=random.randint(1, 48))).isoformat(),
            "collected_at": datetime.utcnow().isoformat(),
            "heat_score": base["heat_score"],
            "is_alert": base["severity"] in ["high", "critical"]
        }
        events.append(event)
    
    return events

MOCK_EVENTS = generate_mock_events()


@router.get("/list", summary="获取事件列表")
async def get_events(
    limit: int = Query(50, ge=1, le=200),
    region: Optional[str] = None,
    category: Optional[str] = None,
    severity: Optional[str] = None,
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db)
):
    """获取全球事件列表"""
    # 使用模拟数据
    events = MOCK_EVENTS[:limit]
    
    if region:
        events = [e for e in events if e["region"] == region]
    if category:
        events = [e for e in events if e["category"] == category]
    if severity:
        events = [e for e in events if e["severity"] == severity]
    
    return {
        "code": 0,
        "data": events,
        "total": len(events)
    }


@router.get("/{event_id}", summary="获取事件详情")
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """获取单个事件详情"""
    events = [e for e in MOCK_EVENTS if e["id"] == event_id]
    if not events:
        raise HTTPException(status_code=404, detail="事件不存在")
    
    return {
        "code": 0,
        "data": events[0]
    }


@router.get("/stats/overview", summary="获取统计概览")
async def get_stats(db: Session = Depends(get_db)):
    """获取统计概览"""
    # 模拟统计数据
    region_counts = {}
    category_counts = {}
    alert_count = 0
    
    for event in MOCK_EVENTS:
        region = event["region"]
        category = event["category"]
        region_counts[region] = region_counts.get(region, 0) + 1
        category_counts[category] = category_counts.get(category, 0) + 1
        if event["is_alert"]:
            alert_count += 1
    
    return {
        "code": 0,
        "data": {
            "total_events": len(MOCK_EVENTS),
            "alert_events": alert_count,
            "by_region": [{"region": r, "count": c} for r, c in region_counts.items()],
            "by_category": [{"category": c, "count": n} for c, n in category_counts.items()]
        }
    }
