# 天眼 SkyEye - 后端服务

## 🚀 快速启动

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

## 📁 目录结构

```
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── api/
│   └── services/
│       ├── world_monitor.py
│       ├── cloudflare_radar.py
│       └── analyzer.py
├── requirements.txt
└── .env
```

## 🔧 技术栈

- **框架：** FastAPI
- **数据库：** MySQL 8.0
- **缓存：** Redis
- **爬虫：** httpx + BeautifulSoup
- **分析：** NLP 情感分析
