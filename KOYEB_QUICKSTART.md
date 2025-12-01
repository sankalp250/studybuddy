# 🚀 Koyeb Quick Start (5 Minutes!)

Deploy your StudyBuddy backend to Koyeb with **NO CREDIT CARD** required!

---

## Step 1️⃣: Push Code to GitHub

```bash
cd d:\studybuddy
git add .
git commit -m "Ready for Koyeb deployment"
git push origin main
```

---

## Step 2️⃣: Create Koyeb Account

1. Go to **[koyeb.com](https://www.koyeb.com/)**
2. Click **"Sign up"** with GitHub
3. Authorize Koyeb
4. **No credit card needed!** ✅

---

## Step 3️⃣: Create New App

1. Click **"Create App"**
2. Select **"GitHub"** → Choose your repo: `studybuddy`
3. Select branch: `main`

---

## Step 4️⃣: Configure Build

- **Builder**: `Dockerfile`
- **Port**: `8000`
- **Health Check**: `/`

---

## Step 5️⃣: Add Environment Variables

Click **"Environment Variables"** and add:

```
SECRET_KEY = (generate with: python -c "import secrets; print(secrets.token_hex(32))")
GROQ_API_KEY = your-groq-api-key
TAVILY_API_KEY = your-tavily-api-key
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60
```

---

## Step 6️⃣: Add PostgreSQL Database

1. Go to **"Databases"** → **"Create Database"**
2. Choose **PostgreSQL** (Free tier - 256MB)
3. Name: `studybuddy-db`
4. Click **"Create"**
5. Copy the **Connection String**
6. Add to app environment variables as `DATABASE_URL`

---

## Step 7️⃣: Deploy!

1. Click **"Deploy"**
2. Wait 3-5 minutes ⏱️
3. Done! 🎉

---

## Step 8️⃣: Test Your API

Your app URL: `https://studybuddy-backend-YOUR-ID.koyeb.app`

```bash
# Test health check
curl https://your-app.koyeb.app/

# View API docs
# Open: https://your-app.koyeb.app/docs
```

---

## Step 9️⃣: Update Streamlit Frontend

```python
BACKEND_URL = "https://your-app.koyeb.app"
```

---

## ✅ Done!

Your backend is live! 🚀

**Free tier includes:**
- 512MB RAM
- 100GB bandwidth/month
- Free PostgreSQL (256MB)
- Auto-deploy from GitHub
- **NO CREDIT CARD!** 🎉

---

**For detailed guide, see [KOYEB_DEPLOYMENT.md](KOYEB_DEPLOYMENT.md)**
