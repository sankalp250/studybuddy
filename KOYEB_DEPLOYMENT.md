# 🚀 Deploy StudyBuddy Backend to Koyeb (No Credit Card Required!)

Koyeb is a modern serverless platform that offers a **truly free tier** with no credit card required. Perfect for deploying your FastAPI backend!

---

## ✨ Why Koyeb?

✅ **Free Tier (Forever):**
- 1 web service (always-on)
- 512MB RAM, 0.1 vCPU
- 2.5GB storage
- 100GB bandwidth/month
- **NO CREDIT CARD REQUIRED!** 🎉

✅ **Features:**
- Native Docker support
- Auto-deploy from GitHub
- Free PostgreSQL database
- Automatic HTTPS & SSL
- Global CDN
- Fast cold starts

---

## 📋 What You'll Need

- GitHub account (with your code)
- Koyeb account (free, no CC needed)
- 10 minutes of time ⏱️

---

## 🎯 Step-by-Step Deployment

### Step 1: Create Koyeb Account

1. Go to **[koyeb.com](https://www.koyeb.com/)**
2. Click **"Sign up for free"**
3. Choose **GitHub** to sign up (easiest)
4. Authorize Koyeb to access your repositories
5. **No credit card required!** ✅

---

### Step 2: Push Your Code to GitHub

Make sure your latest code is on GitHub:

```bash
cd d:\studybuddy
git add .
git commit -m "Ready for Koyeb deployment"
git push origin main
```

---

### Step 3: Create New App on Koyeb

1. In Koyeb dashboard, click **"Create App"**
2. Choose **"GitHub"** as the source
3. Select your repository: **`studybuddy`**
4. Choose branch: **`main`**

---

### Step 4: Configure Build Settings

**Builder:** Select **"Dockerfile"**
- Koyeb will automatically detect your `Dockerfile`

**Exposed Port:** `8000`
- This is the port your FastAPI app runs on

**Health Check Path:** `/`
- Koyeb will ping this endpoint to check if your app is healthy

---

### Step 5: Add Environment Variables

Click **"Environment Variables"** and add these:

| Variable Name | Value |
|---------------|-------|
| `DATABASE_URL` | (We'll add PostgreSQL in next step) |
| `SECRET_KEY` | Your JWT secret key |
| `GROQ_API_KEY` | Your Groq API key |
| `TAVILY_API_KEY` | Your Tavily API key |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` |

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

⚠️ **Note:** We'll add `DATABASE_URL` in the next step when we create the database.

---

### Step 6: Add PostgreSQL Database

1. In Koyeb dashboard, go to **"Databases"**
2. Click **"Create Database"**
3. Choose **"PostgreSQL"**
4. Select **Free tier** (256MB)
5. Name it: `studybuddy-db`
6. Click **"Create"**

**Once created:**
1. Click on your database
2. Copy the **Connection String** (starts with `postgresql://`)
3. Go back to your app → **Environment Variables**
4. Add `DATABASE_URL` with the connection string

---

### Step 7: Deploy!

1. Review your settings
2. Click **"Deploy"**
3. Wait 3-5 minutes for deployment

Koyeb will:
- Build your Docker image
- Run database migrations
- Start your application
- Perform health checks

---

### Step 8: Get Your App URL

Once deployed, you'll see your app URL:

```
https://studybuddy-backend-YOUR-ID.koyeb.app
```

**Test it:**
```bash
curl https://studybuddy-backend-YOUR-ID.koyeb.app/
# Expected: {"message": "Welcome to the StudyBuddy AI API!"}
```

---

## 🧪 Testing Your Deployment

### 1. Health Check
```bash
curl https://your-app.koyeb.app/
```

### 2. API Documentation
Open in browser:
```
https://your-app.koyeb.app/docs
```

You should see **FastAPI Swagger UI**!

### 3. Test User Registration
```bash
curl -X POST "https://your-app.koyeb.app/api/users/" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'
```

### 4. Test Login
```bash
curl -X POST "https://your-app.koyeb.app/api/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpass123"
```

---

## 🔄 Update Your Streamlit Frontend

Update your Streamlit configuration:

**In Streamlit Cloud Secrets:**
```toml
BACKEND_URL = "https://your-app.koyeb.app"
```

**Or in your code:**
```python
BACKEND_URL = "https://your-app.koyeb.app"
```

---

## 📊 Monitoring & Management

### View Logs
1. Go to your app in Koyeb dashboard
2. Click **"Logs"** tab
3. See real-time logs

### Check Metrics
1. Click **"Metrics"** tab
2. View CPU, Memory, Network usage

### Redeploy
1. Push changes to GitHub
2. Koyeb **auto-deploys** automatically! 🎉

Or manually redeploy:
1. Go to app settings
2. Click **"Redeploy"**

---

## 🐛 Troubleshooting

### Build Fails

**Check logs:**
1. Go to app → **Deployments**
2. Click on failed deployment
3. View build logs

**Common issues:**
- Missing dependencies in `requirements.txt`
- Dockerfile errors
- Port configuration (should be 8000)

---

### Database Connection Errors

**Verify DATABASE_URL:**
1. Go to app → **Environment Variables**
2. Check `DATABASE_URL` is set correctly
3. Format should be: `postgresql://user:pass@host:port/db`

**Test connection:**
1. Check database status in **Databases** tab
2. Ensure it's running (green status)

---

### App Not Responding

**Check health:**
1. Go to app dashboard
2. Check status (should be green)
3. View **Health Checks** tab

**Restart app:**
1. Go to app settings
2. Click **"Restart"**

---

### Migration Errors

If you see "Can't locate revision" errors:

Your `start.sh` already handles this! But if needed:
1. Go to app → **Terminal** (if available)
2. Run: `alembic stamp head`
3. Restart app

---

## ⚡ Performance Tips

### Auto-Deploy on Push
Already configured! Every time you push to GitHub:
```bash
git push origin main
```

Koyeb automatically rebuilds and redeploys! 🚀

### Monitor Free Tier Usage
1. Go to **Billing** tab
2. Check usage:
   - RAM: 512MB limit
   - Bandwidth: 100GB/month
   - Storage: 2.5GB

---

## 🆚 Koyeb vs Other Platforms

| Feature | Koyeb | Fly.io | Render |
|---------|-------|--------|--------|
| **Credit Card** | ❌ No | ✅ Required | ⚠️ After trial |
| **Free RAM** | 512MB | 256MB | 512MB |
| **Docker Support** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Auto Deploy** | ✅ Yes | ⚠️ Manual | ✅ Yes |
| **Free Database** | ✅ PostgreSQL | ✅ PostgreSQL | ✅ PostgreSQL |
| **Cold Starts** | Fast (~5s) | Very Fast (~3s) | Slow (~30s) |

**Verdict:** Koyeb is the best **no-credit-card** option! 🏆

---

## 🔒 Security Best Practices

### 1. Secure SECRET_KEY
Always use a strong, randomly generated key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Limit CORS Origins
In `main.py`, update to your Streamlit domain:
```python
allow_origins=["https://your-app.streamlit.app"]
```

### 3. Use Environment Variables
Never hardcode API keys in your code!

---

## 📚 Resources

- [Koyeb Documentation](https://www.koyeb.com/docs)
- [Koyeb API Reference](https://www.koyeb.com/docs/api)
- [Koyeb Community](https://community.koyeb.com/)
- [Koyeb Status](https://status.koyeb.com/)

---

## ✅ Deployment Checklist

- [ ] Create Koyeb account (no CC needed!)
- [ ] Push code to GitHub
- [ ] Create new app on Koyeb
- [ ] Configure Dockerfile builder
- [ ] Set exposed port to 8000
- [ ] Add environment variables (SECRET_KEY, API keys)
- [ ] Create PostgreSQL database
- [ ] Add DATABASE_URL to environment
- [ ] Deploy app
- [ ] Test health check endpoint
- [ ] Test `/docs` API documentation
- [ ] Test user registration & login
- [ ] Update Streamlit frontend URL
- [ ] Test end-to-end flow

---

## 🎉 Success!

Your StudyBuddy backend is now live on Koyeb!

**Your API URL:** `https://your-app.koyeb.app`

**Benefits you get:**
- ✅ Free forever (no credit card)
- ✅ Auto-deploy from GitHub
- ✅ Free PostgreSQL database
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Easy monitoring

Happy deploying! 🚀
