"""
World Monitor 数据采集服务
https://www.worldmonitor.app/
"""
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime

class WorldMonitorCollector:
    """World Monitor 数据采集器"""
    
    def __init__(self):
        self.base_url = "https://www.worldmonitor.app/"
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "User-Agent": "Mozilla/5.0 (WorldWatch Intelligence System)"
            }
        )
    
    async def close(self):
        await self.client.aclose()
    
    async def get_global_events(self, limit: int = 50) -> List[Dict]:
        """
        获取全球事件
        
        返回：
        [
            {
                "title": "事件标题",
                "region": "地区",
                "country": "国家",
                "category": "类别",
                "severity": "严重程度",
                "summary": "摘要",
                "source_url": "来源链接",
                "publish_time": "发布时间",
                "collected_at": "采集时间"
            }
        ]
        """
        events = []
        
        try:
            # 访问 World Monitor 首页
            response = await self.client.get(self.base_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                
                # 解析事件列表（根据实际页面结构调整）
                event_cards = soup.find_all('div', class_='event-card')
                
                for card in event_cards[:limit]:
                    event = {
                        "title": card.find('h3').text.strip() if card.find('h3') else "",
                        "region": card.find('span', class_='region').text.strip() if card.find('span', class_='region') else "Unknown",
                        "country": card.find('span', class_='country').text.strip() if card.find('span', class_='country') else "",
                        "category": card.find('span', class_='category').text.strip() if card.find('span', class_='category') else "Other",
                        "severity": self._parse_severity(card),
                        "summary": card.find('p', class_='summary').text.strip() if card.find('p', class_='summary') else "",
                        "source_url": card.find('a')['href'] if card.find('a') else "",
                        "publish_time": self._parse_time(card),
                        "collected_at": datetime.now().isoformat(),
                        "source": "world_monitor"
                    }
                    events.append(event)
                
                print(f"✅ World Monitor 采集：{len(events)} 个事件")
            else:
                print(f"❌ World Monitor 请求失败：{response.status_code}")
        
        except Exception as e:
            print(f"❌ World Monitor 采集失败：{e}")
        
        return events
    
    def _parse_severity(self, card) -> str:
        """解析事件严重程度"""
        severity_map = {
            'critical': '严重',
            'high': '高',
            'medium': '中',
            'low': '低'
        }
        # 根据实际页面结构解析
        return "medium"
    
    def _parse_time(self, card) -> str:
        """解析时间"""
        time_elem = card.find('time')
        if time_elem:
            return time_elem.get('datetime', datetime.now().isoformat())
        return datetime.now().isoformat()


# 单例
collector = WorldMonitorCollector()
