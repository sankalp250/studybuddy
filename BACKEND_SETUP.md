# Backend Setup & Connection Guide

## 🎯 How to Know if Your Render Backend is Running

### Method 1: Check Render Dashboard
1. Log in to https://dashboard.render.com/
2. Open your backend service
3. Check the service status — it should be "Live"
4. View the logs to verify the backend started

### Method 2: Test the API Endpoint
Run this command in your terminal:
```bash
curl https://your-backend-url.onrender.com/
```

You should see:
```json
{"message": "Welcome to the StudyBuddy AI API!"}
```

### Method 3: Check the Health Endpoint
```bash
curl https://your-backend-url.onrender.com/docs
```

This should show the FastAPI documentation page.

---

## 🏠 Local Development Setup

### Option 1: Using Docker Compose (Recommended)
```bash
# Start backend and database
docker-compose up backend

# Backend will run on http://localhost:8000
```

### Option 2: Run Backend Manually
```bash
# Activate virtual environment
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Linux/Mac

# Set environment variables
export DATABASE_URL=sqlite:///studybuddy.db
export SECRET_KEY=your-local-secret-key
export GROQ_API_KEY=your-key
export TAVILY_API_KEY=your-key
export ACCESS_TOKEN_EXPIRE_MINUTES=60
export ALGORITHM=HS256

# Run migrations
alembic upgrade head

# Start backend server
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 🚀 Production Deployment Setup

### Step 1: Configure Frontend (Streamlit Cloud)
1. Go to https://share.streamlit.io/
2. Open your app settings
3. Go to "Secrets"
4. Add this configuration:
```toml
[secrets]
BACKEND_URL = "https://your-backend-url.onrender.com"
```

### Step 2: Verify Backend Environment Variables
In Render dashboard, make sure these are set:
```env
DATABASE_URL=postgresql://user:pass@host:port/dbname
SECRET_KEY=your-production-secret-key
GROQ_API_KEY=your-key
TAVILY_API_KEY=your-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALGORITHM=HS256
```

### Step 3: Test Connection
After deploying, test the backend:
```bash
# Test health endpoint
curl https://your-backend-url.onrender.com/

# Test API documentation
open https://your-backend-url.onrender.com/docs
```

---

## 🔧 Troubleshooting Connection Issues

### Error: "Connection refused"
**Problem**: Backend is not running or not accessible.

**Solutions**:
1. Check if the backend service is running in Render dashboard
2. Verify the backend URL is correct
3. Ensure the backend allows CORS from your frontend domain

### Error: "Connection timeout"
**Problem**: Network issue or backend is taking too long to respond.

**Solutions**:
1. Render free tier services spin down after inactivity
2. The first request may take 30-60 seconds to wake up the service
3. Check Render logs for errors

### Error: "401 Unauthorized"
**Problem**: Authentication token issue.

**Solutions**:
1. Clear your browser cookies and try logging in again
2. Verify SECRET_KEY matches between frontend and backend
3. Check if token has expired

---

## 📋 Quick Test Commands

### Test Backend is Running
```bash
# Test 1: Check if backend responds
curl https://your-backend-url.onrender.com/

# Test 2: Check API docs
curl https://your-backend-url.onrender.com/docs

# Test 3: Try login endpoint
curl -X POST https://your-backend-url.onrender.com/api/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=test123"
```

### Test Frontend Connection
```bash
# Check what backend URL your frontend is using
# Open browser console and type:
# window.location.href
```

---

## 🎯 Configuration Priority

The backend URL is determined in this order:
1. **Streamlit Secrets** (for deployed apps): `st.secrets["BACKEND_URL"]`
2. **Environment Variable**: `BACKEND_URL` environment variable
3. **Default**: `http://127.0.0.1:8000` (for local development)

---

## ✅ Checklist

- [ ] Backend deployed on Render and status is "Live"
- [ ] Environment variables configured in Render
- [ ] Frontend secrets configured in Streamlit Cloud
- [ ] Test endpoint returns: `{"message": "Welcome to the StudyBuddy AI API!"}`
- [ ] Can access API docs at `/docs` endpoint
- [ ] Frontend can connect and show no connection errors

---

## 📞 Need Help?

If you're still having issues:
1. Check Render dashboard logs for backend errors
2. Check Streamlit Cloud logs for frontend errors
3. Verify all environment variables are set correctly
4. Ensure backend and frontend are using compatible API versions
