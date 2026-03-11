"""
全球新闻数据采集服务 - 免费数据源
支持：Reddit, RSS, 公开新闻源
"""
import httpx
import feedparser
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import asyncio

class GlobalNewsCollector:
    """全球新闻采集器"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "User-Agent": "Mozilla/5.0 (WorldWatch Global Monitor)"
            }
        )
        
        # RSS 新闻源列表（优化：包含国内可访问源）
        self.rss_feeds = [
            # 国内可访问（速度快）
            {"name": "IT 之家", "url": "https://www.ithome.com/rss/", "region": "亚洲"},
            {"name": "36Kr", "url": "https://36kr.com/feed", "region": "亚洲"},
            
            # 国际新闻（可能慢但重要）
            {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "region": "北美"},
            {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "region": "北美"},
        ]
        
        # Reddit API（免费，无需 Key）
        self.reddit_base = "https://www.reddit.com"
        self.subreddits = [
            {"name": "worldnews", "url": "/r/worldnews/top.json?limit=25&t=day", "category": "政治"},
            {"name": "news", "url": "/r/news/top.json?limit=25&t=day", "category": "新闻"},
            {"name": "technology", "url": "/r/technology/top.json?limit=25&t=day", "category": "科技"},
            {"name": "science", "url": "/r/science/top.json?limit=25&t=day", "category": "科技"},
            {"name": "environment", "url": "/r/environment/top.json?limit=25&t=day", "category": "环境"},
            {"name": "economy", "url": "/r/Economics/top.json?limit=25&t=day", "category": "经济"},
        ]
    
    async def close(self):
        await self.client.aclose()
    
    async def collect_rss_news(self, limit: int = 50) -> List[Dict]:
        """从 RSS 源采集新闻"""
        all_news = []
        
        tasks = [self._fetch_rss_feed(feed) for feed in self.rss_feeds]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                all_news.extend(result)
        
        # 按时间排序，取最新
        all_news.sort(key=lambda x: x.get("publish_time", ""), reverse=True)
        return all_news[:limit]
    
    async def _fetch_rss_feed(self, feed_info: Dict) -> List[Dict]:
        """获取单个 RSS 源"""
        news_list = []
        try:
            response = await self.client.get(feed_info["url"])
            if response.status_code == 200:
                feed = feedparser.parse(response.text)
                
                for entry in feed.entries[:10]:
                    news = {
                        "title": entry.title,
                        "summary": entry.get("summary", "")[:500],
                        "source_url": entry.get("link", ""),
                        "source": feed_info["name"],
                        "region": feed_info["region"],
                        "category": "新闻",
                        "publish_time": self._parse_rss_time(entry),
                        "collected_at": datetime.utcnow().isoformat(),
                        "severity": "low",
                        "country": "",
                        "heat_score": 50.0,
                        "is_alert": False
                    }
                    news_list.append(news)
                
                print(f"✅ {feed_info['name']} 采集：{len(news_list)} 条")
        except Exception as e:
            print(f"❌ {feed_info['name']} 采集失败：{e}")
        
        return news_list
    
    async def collect_reddit_posts(self, limit: int = 50) -> List[Dict]:
        """从 Reddit 采集热门帖子"""
        all_posts = []
        
        tasks = [self._fetch_subreddit(sub) for sub in self.subreddits]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                all_posts.extend(result)
        
        # 按热度排序
        all_posts.sort(key=lambda x: x.get("heat_score", 0), reverse=True)
        return all_posts[:limit]
    
    async def _fetch_subreddit(self, subreddit: Dict) -> List[Dict]:
        """获取单个 Subreddit"""
        posts = []
        try:
            url = f"{self.reddit_base}{subreddit['url']}"
            response = await self.client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                for post in data.get("data", {}).get("children", []):
                    post_data = post.get("data", {})
                    score = post_data.get("score", 0)
                    
                    # 计算热度分数 (0-100)
                    heat_score = min(100, score / 100)
                    
                    news = {
                        "title": post_data.get("title", ""),
                        "summary": post_data.get("selftext", "")[:500],
                        "source_url": f"https://reddit.com{post_data.get('permalink', '')}",
                        "source": f"r/{subreddit['name']}",
                        "region": "全球",
                        "category": subreddit["category"],
                        "publish_time": datetime.fromtimestamp(post_data.get("created_utc", 0)).isoformat(),
                        "collected_at": datetime.utcnow().isoformat(),
                        "severity": self._calc_severity(score),
                        "country": "",
                        "heat_score": heat_score,
                        "is_alert": heat_score > 80
                    }
                    posts.append(news)
                
                print(f"✅ r/{subreddit['name']} 采集：{len(posts)} 条")
        except Exception as e:
            print(f"❌ r/{subreddit['name']} 采集失败：{e}")
        
        return posts
    
    def _parse_rss_time(self, entry) -> str:
        """解析 RSS 时间"""
        try:
            import email.utils
            time_tuple = email.utils.parsedate_tz(entry.published)
            if time_tuple:
                dt = datetime(*time_tuple[:6])
                return dt.isoformat()
        except:
            pass
        return datetime.utcnow().isoformat()
    
    def _calc_severity(self, score: int) -> str:
        """根据热度计算严重程度"""
        if score > 10000:
            return "critical"
        elif score > 5000:
            return "high"
        elif score > 1000:
            return "medium"
        return "low"
    
    async def collect_all(self, rss_limit: int = 30, reddit_limit: int = 30) -> List[Dict]:
        """采集所有数据源"""
        rss_news, reddit_posts = await asyncio.gather(
            self.collect_rss_news(rss_limit),
            self.collect_reddit_posts(reddit_limit),
            return_exceptions=True
        )
        
        all_events = []
        if isinstance(rss_news, list):
            all_events.extend(rss_news)
        if isinstance(reddit_posts, list):
            all_events.extend(reddit_posts)
        
        # 按热度排序
        all_events.sort(key=lambda x: x.get("heat_score", 0), reverse=True)
        return all_events


# 单例
collector = GlobalNewsCollector()
