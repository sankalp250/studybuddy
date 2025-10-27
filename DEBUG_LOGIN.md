# Login 500 Error - Debug Version

## Added Debugging Features

I've updated the login system to help identify what's causing the 500 error:

### 1. **Better Error Messages**
- The backend now shows detailed error messages
- Includes full traceback in server logs
- Catches and reports specific failure points

### 2. **Frontend Debug Mode**
- Added a "Show Debug Info" checkbox in the sidebar
- Shows which URL is being used for API calls
- Displays response status and error details
- Shows full exception information

### How to Use:

1. **Start the backend** (if not running):
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

2. **Start the frontend**:
```bash
streamlit run dashboard.py
```

3. **Enable Debug Mode**:
   - Go to the Account page
   - Check the "Show Debug Info" checkbox in the sidebar
   - You'll see the exact URL being used and response details

4. **Try logging in**:
   - Use: `sankalp25027@gmail.com` / `test123`
   - Check the debug info to see what's happening

### Expected URLs:
- Backend URL: `http://127.0.0.1:8000`
- API URL: `http://127.0.0.1:8000/api`
- Token URL: `http://127.0.0.1:8000/api/token`

### Check Backend Logs:
When you try to login, the backend will print detailed error messages to the console. Look for:
- "Login error: ..." messages
- Full stack traces showing where the error occurred

### Test Directly:
You can also test the login endpoint directly:
```bash
python scripts/debug_login.py sankalp25027@gmail.com test123
```

This will show you if the issue is with the endpoint itself or the Streamlit frontend.
