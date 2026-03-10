# WorldWatch 天眼 - 部署到 Render

## 🚀 一键部署

1. 访问 https://render.com
2. 注册/登录账号（支持 GitHub 登录）
3. 点击 "New +" → "Web Service"
4. 连接 GitHub 仓库或上传代码

## 📦 快速部署方案

### 方案 A: 使用 Render（推荐）

```bash
# 1. 将代码推送到 GitHub
cd ~/.openclaw/workspace/skyeye
git init
git add .
git commit -m "WorldWatch MVP"
git remote add origin <你的 GitHub 仓库>
git push -u origin main

# 2. 在 Render 部署
- 选择 "Public Git repository"
- 选择你的仓库
- Build Command: pip install -r backend/requirements.txt
- Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
- 选择免费套餐
```

### 方案 B: 使用 Railway

```bash
# 1. 访问 https://railway.app
# 2. 登录 GitHub
# 3. 选择 "New Project" → "Deploy from GitHub repo"
# 4. 自动识别 Python 并部署
```

### 方案 C: 使用 Vercel（最简单）

```bash
# 1. 安装 Vercel CLI
npm install -g vercel

# 2. 部署
cd ~/.openclaw/workspace/skyeye/backend
vercel --prod
```

## 🌐 免费额度

| 平台 | 免费额度 | 域名 |
|------|---------|------|
| Render | 750 小时/月 | .onrender.com |
| Railway | $5/月 | .railway.app |
| Vercel | 无限 | .vercel.app |

## ⚡ 最快方案

**使用 Vercel** - 3 分钟上线：

```bash
cd ~/.openclaw/workspace/skyeye/backend
npm install -g vercel
vercel --prod
```

会自动生成类似：`https://worldwatch-xxx.vercel.app`
