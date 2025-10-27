# Quick Start Guide - Check If Your Backend is Running

## 🎯 Quick Answer: Is My Backend Running?

Run this command to check:
```bash
python scripts/test_backend_connection.py
```

If you see:
```
[SUCCESS] Backend is ready to use!
```
Your backend is running! ✅

---

## 📋 Complete Checklist

### ✅ Your Backend is Running if:
1. ✅ Test script shows `[SUCCESS] Backend is ready to use!`
2. ✅ You can visit `http://127.0.0.1:8000/docs` in your browser
3. ✅ Streamlit app doesn't show "Connection failed" error

### ❌ Your Backend is NOT Running if:
1. ❌ Test script shows `[FAILED]` messages
2. ❌ Browser can't connect to `http://127.0.0.1:8000`
3. ❌ Streamlit shows "Connection refused" error

---

## 🚀 How to Start Your Backend

### Option 1: Docker (Easiest)
```bash
docker-compose up backend
```

### Option 2: Manual Start
```bash
# Activate virtual environment
venv\Scripts\activate

# Run backend
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 🌐 For Render Backend (Production)

### Check if Render Backend is Running:
1. **Visit Render Dashboard**: https://dashboard.render.com/
2. **Check service status** - should be "Live"
3. **Test with:** `python scripts/test_backend_connection.py https://your-backend.onrender.com`

---

## 🔧 What Was Fixed

- ✅ All pages now use **configurable backend URL**
- ✅ Works with **localhost** for local development
- ✅ Works with **Render URL** for production
- ✅ Automatically detects which environment you're in

### Files Updated:
- `dashboard.py` - Main app configuration
- `pages/01_🎯_Todo_List.py` - Todo page
- `pages/02_📰_Daily_Digest.py` - Digest page
- `pages/03_💻_LeetCode_Practice.py` - LeetCode page
- `pages/04_👤_Account.py` - Account page
- `pages/05_🧠_SRS_Review.py` - Review page

---

## 🧪 Test Commands

### Test Backend Connection
```bash
# Test local backend
python scripts/test_backend_connection.py

# Test Render backend
python scripts/test_backend_connection.py https://your-backend.onrender.com
```

### Start Everything
```bash
# Terminal 1: Start backend
uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Start frontend
streamlit run dashboard.py
```

---

## 📖 More Information

- **Detailed setup**: See `BACKEND_SETUP.md`
- **What changed**: See `CHANGES_SUMMARY.md`
- **Troubleshooting**: See `BACKEND_SETUP.md`

---

## 💡 Quick Tips

1. **Always test backend first**: Run the test script before starting the frontend
2. **Check the docs**: Visit `http://127.0.0.1:8000/docs` to verify
3. **Watch for errors**: Connection errors mean backend is not running
4. **Restart if needed**: If connection fails, restart the backend

---

## 🆘 Troubleshooting

### Error: "Connection refused"
- **Fix**: Backend is not running → Start it with `uvicorn main:app`

### Error: "Connection timeout"
- **Fix**: Render free tier is sleeping → Wait 30-60 seconds

### Error: "401 Unauthorized"
- **Fix**: Token expired → Clear cookies and login again

---

**Need help? Check `BACKEND_SETUP.md` for detailed troubleshooting!**
