"""
事件管理 API - 真实数据源
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
import asyncio

from app.services.news_collector import collector as news_collector

router = APIRouter()

# 内存缓存（简化版，生产环境用 Redis）
_cached_events = []
_last_update = None
CACHE_DURATION = timedelta(minutes=10)  # 10 分钟更新一次


async def get_fresh_events():
    """获取最新事件（带缓存）"""
    global _cached_events, _last_update
    
    now = datetime.utcnow()
    
    # 检查缓存是否过期
    if _cached_events and _last_update and (now - _last_update) < CACHE_DURATION:
        return _cached_events
    
    # 采集新数据
    try:
        events = await news_collector.collect_all(rss_limit=30, reddit_limit=30)
        _cached_events = events
        _last_update = now
        print(f"✅ 数据更新：{len(events)} 条事件，缓存至 {_last_update}")
    except Exception as e:
        print(f"❌ 数据采集失败：{e}")
        # 返回旧缓存（如果有）
        if not _cached_events:
            # 首次失败，返回模拟数据
            _cached_events = generate_fallback_events()
    
    return _cached_events


def generate_fallback_events():
    """备用模拟数据（当真实数据源失败时）"""
    base_events = [
        {
            "title": "全球科技巨头发布新一代 AI 芯片，性能提升 300%",
            "region": "北美",
            "category": "科技",
            "severity": "medium",
            "summary": "多家科技巨头今日同时发布新一代 AI 芯片，采用 3nm 工艺。",
            "source_url": "https://techcrunch.com",
            "source": "TechCrunch",
            "publish_time": datetime.utcnow().isoformat(),
            "collected_at": datetime.utcnow().isoformat(),
            "heat_score": 85.5,
            "is_alert": False,
            "country": ""
        },
        {
            "title": "某国央行宣布加息 50 个基点，全球金融市场震荡",
            "region": "欧洲",
            "category": "经济",
            "severity": "high",
            "summary": "为应对持续高通胀，该国央行宣布加息 50 个基点。",
            "source_url": "https://reuters.com",
            "source": "Reuters",
            "publish_time": datetime.utcnow().isoformat(),
            "collected_at": datetime.utcnow().isoformat(),
            "heat_score": 92.3,
            "is_alert": True,
            "country": ""
        },
    ]
    return base_events


@router.get("/list", summary="获取事件列表")
async def get_events(
    limit: int = Query(50, ge=1, le=200),
    region: Optional[str] = None,
    category: Optional[str] = None,
    severity: Optional[str] = None,
):
    """获取全球事件列表（真实数据源）"""
    events = await get_fresh_events()
    
    # 筛选
    if region:
        events = [e for e in events if e.get("region") == region]
    if category:
        events = [e for e in events if e.get("category") == category]
    if severity:
        events = [e for e in events if e.get("severity") == severity]
    
    return {
        "code": 0,
        "data": events[:limit],
        "total": len(events),
        "last_update": _last_update.isoformat() if _last_update else None
    }


@router.get("/{event_id}", summary="获取事件详情")
async def get_event(event_id: int):
    """获取单个事件详情"""
    events = await get_fresh_events()
    
    if event_id < 0 or event_id >= len(events):
        raise HTTPException(status_code=404, detail="事件不存在")
    
    return {
        "code": 0,
        "data": events[event_id]
    }


@router.get("/stats/overview", summary="获取统计概览")
async def get_stats():
    """获取统计概览"""
    events = await get_fresh_events()
    
    # 统计数据
    region_counts = {}
    category_counts = {}
    alert_count = 0
    
    for event in events:
        region = event.get("region", "未知")
        category = event.get("category", "未知")
        region_counts[region] = region_counts.get(region, 0) + 1
        category_counts[category] = category_counts.get(category, 0) + 1
        if event.get("is_alert", False):
            alert_count += 1
    
    return {
        "code": 0,
        "data": {
            "total_events": len(events),
            "alert_events": alert_count,
            "by_region": [{"region": r, "count": c} for r, c in region_counts.items()],
            "by_category": [{"category": c, "count": n} for c, n in category_counts.items()],
            "last_update": _last_update.isoformat() if _last_update else None
        }
    }


@router.post("/refresh", summary="手动刷新数据")
async def refresh_data():
    """手动触发数据采集"""
    global _cached_events, _last_update
    _cached_events = []
    _last_update = None
    events = await get_fresh_events()
    return {
        "code": 0,
        "message": f"已刷新 {len(events)} 条事件",
        "data": {"count": len(events), "update_time": _last_update.isoformat() if _last_update else None}
    }
