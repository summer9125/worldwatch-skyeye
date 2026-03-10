# 🚀 WorldWatch 天眼 - 一键部署指南

## 📦 部署包内容

```
skyeye/
├── backend/              # 后端代码
│   ├── app/
│   │   ├── main.py      # FastAPI 入口
│   │   ├── config.py    # 配置
│   │   ├── database.py  # 数据库
│   │   ├── models.py    # 数据模型
│   │   ├── api/         # API 路由
│   │   └── static/      # 前端页面
│   ├── requirements.txt # Python 依赖
│   └── .env            # 环境配置
├── vercel.json          # Vercel 配置
└── README.md           # 部署说明
```

---

## ⚡ 方案 1: Vercel 部署（推荐，3 分钟）

### 步骤 1: 准备代码

将 `skyeye` 文件夹上传到 GitHub：

```bash
cd ~/.openclaw/workspace/skyeye
git init
git add .
git commit -m "WorldWatch MVP"
git remote add origin https://github.com/你的用户名/worldwatch.git
git push -u origin main
```

### 步骤 2: Vercel 部署

1. 访问 **https://vercel.com**
2. 点击 **"Sign Up"** 用 GitHub 登录
3. 点击 **"Add New Project"**
4. 选择 **"Import Git Repository"**
5. 选择你的 `worldwatch` 仓库
6. 点击 **"Deploy"**

### 步骤 3: 配置环境变量

在 Vercel 项目设置中添加：

```
DATABASE_URL=sqlite:///./worldwatch.db
PORT=8002
```

### 步骤 4: 完成

等待 2-3 分钟，Vercel 会生成类似这样的域名：

**https://worldwatch-xxx.vercel.app**

---

## 🎯 方案 2: Railway 部署（5 分钟）

### 步骤 1: 登录 Railway

1. 访问 **https://railway.app**
2. 用 GitHub 登录

### 步骤 2: 创建项目

1. 点击 **"New Project"**
2. 选择 **"Deploy from GitHub repo"**
3. 选择你的 `worldwatch` 仓库

### 步骤 3: 配置

Railway 会自动识别 Python 并安装依赖。

添加环境变量：
```
DATABASE_URL=sqlite:///./worldwatch.db
PORT=$PORT
```

### 步骤 4: 部署

点击 **"Deploy"**，等待完成后会生成域名：

**https://worldwatch-production.up.railway.app**

---

## 🌐 方案 3: Render 部署（5 分钟）

### 步骤 1: 登录 Render

1. 访问 **https://render.com**
2. 用 GitHub 登录

### 步骤 2: 创建 Web Service

1. 点击 **"New +"** → **"Web Service"**
2. 连接你的 GitHub 仓库
3. 配置：
   - **Name**: worldwatch
   - **Environment**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 步骤 3: 环境变量

添加：
```
DATABASE_URL=sqlite:///./worldwatch.db
PORT=8002
```

### 步骤 4: 部署

选择 **Free** 套餐，点击 **"Create Web Service"**

完成后域名：

**https://worldwatch.onrender.com**

---

## ✅ 部署后验证

访问部署后的域名，应该看到：

1. ✅ 专业深色科技风仪表盘
2. ✅ 4 个统计卡片（总事件/告警/地区/风险）
3. ✅ 事件趋势图表
4. ✅ 地区分布环形图
5. ✅ 热点事件列表

API 测试：
- `https://你的域名.com/health`
- `https://你的域名.com/api/v1/events/list`
- `https://你的域名.com/api/v1/events/stats/overview`

---

## 🔧 故障排查

### 问题 1: 页面空白
- 检查浏览器控制台是否有错误
- 确认静态文件路径正确

### 问题 2: API 报错
- 检查环境变量是否配置
- 查看平台日志（Vercel Functions / Railway Logs）

### 问题 3: 数据库错误
- 确认 DATABASE_URL 配置正确
- SQLite 需要可写权限

---

## 📞 需要帮助？

部署过程中遇到任何问题，随时告诉我！

---

**创建时间**: 2026-03-10  
**版本**: v1.0.0  
**作者**: WorldWatch Team
