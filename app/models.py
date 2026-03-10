"""
数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, Index
from datetime import datetime

from app.database import Base


class Event(Base):
    """全球事件表"""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    region = Column(String(100), index=True)
    country = Column(String(100), index=True)
    category = Column(String(50), index=True)
    severity = Column(String(20), default="medium")
    summary = Column(Text)
    content = Column(Text)
    source_url = Column(String(1000))
    source = Column(String(50), default="world_monitor")
    publish_time = Column(DateTime)
    collected_at = Column(DateTime, default=datetime.utcnow, index=True)
    heat_score = Column(Float, default=0.0)
    is_alert = Column(Boolean, default=False)
    
    __table_args__ = (
        Index('idx_region_category', 'region', 'category'),
        Index('idx_publish_time', 'publish_time'),
    )


class Intelligence(Base):
    """情报分析表"""
    __tablename__ = "intelligence"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, index=True)
    analysis_type = Column(String(50))
    analysis_result = Column(Text)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    """告警表"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, index=True)
    alert_level = Column(String(20))
    alert_message = Column(Text)
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
