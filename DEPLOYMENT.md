# 🚀 StudyBuddy AI Deployment Guide

## Phase 1: Docker Setup ✅

### Files Created:
- `Dockerfile` - Backend containerization
- `Dockerfile.frontend` - Frontend containerization  
- `docker-compose.yml` - Local development setup
- `.dockerignore` - Optimized build context

### Test Docker Locally:
```bash
# Build and run with docker-compose
docker-compose up --build

# Or build individual containers
docker build -t studybuddy-backend .
docker build -f Dockerfile.frontend -t studybuddy-frontend .
```

---

## Phase 2: Backend Deployment on Render

### Steps:
1. **Create Render Account**: Sign up at render.com
2. **Create PostgreSQL Database**:
   - Go to Dashboard → New → PostgreSQL
   - Name: `studybuddy-db`
   - Plan: Free tier
   - Note the connection string

3. **Deploy Backend**:
   - Go to Dashboard → New → Web Service
   - Connect your GitHub repository
   - Configure:
     - **Name**: `studybuddy-backend`
     - **Environment**: `Docker`
     - **Dockerfile Path**: `Dockerfile`
     - **Port**: `8000`

4. **Environment Variables**:
   ```env
   DATABASE_URL=postgresql://user:pass@host:port/db
   SECRET_KEY=your-production-secret-key
   GROQ_API_KEY=your-groq-api-key
   TAVILY_API_KEY=your-tavily-api-key
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ALGORITHM=HS256
   ```

5. **Deploy**: Click "Create Web Service"

---

## Phase 3: Frontend Deployment on Streamlit Cloud

### Steps:
1. **Push to GitHub**: Ensure your code is in a GitHub repository
2. **Go to Streamlit Cloud**: https://share.streamlit.io/
3. **Deploy New App**:
   - Connect GitHub account
   - Select repository: `sankalp250/studybuddy-ai`
   - **Main file path**: `dashboard.py`
   - **App URL**: `https://studybuddy-ai.streamlit.app`

4. **Environment Variables** (in Streamlit Cloud):
   ```env
   BACKEND_URL=https://your-render-backend-url.onrender.com
   ```

---

## Phase 4: Hugging Face Spaces (Alternative)

### Steps:
1. **Create Hugging Face Account**: https://huggingface.co/
2. **Create New Space**:
   - Name: `studybuddy-ai`
   - SDK: `Streamlit`
   - Hardware: `CPU Basic` (free)

3. **Upload Files**:
   - Upload your Streamlit files
   - Create `requirements.txt` for Hugging Face
   - Add environment variables in Settings

---

## Environment Variables Reference

### Backend (.env):
```env
DATABASE_URL=postgresql://user:pass@host:port/db
SECRET_KEY=your-super-secret-jwt-key-here
GROQ_API_KEY=your-groq-api-key
TAVILY_API_KEY=your-tavily-api-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```

### Frontend:
```env
BACKEND_URL=https://your-backend-url.onrender.com
```

---

## Testing Deployment

### 1. Test Backend:
```bash
curl https://your-backend-url.onrender.com/
# Should return: {"message": "Welcome to the StudyBuddy AI API!"}
```

### 2. Test Frontend:
- Visit your Streamlit Cloud URL
- Try creating an account
- Test the AI chat functionality

### 3. Test End-to-End:
- Sign up on frontend
- Upload resume
- Create todo items
- Start AI chat sessions

---

## Troubleshooting

### Common Issues:
1. **Database Connection**: Check DATABASE_URL format
2. **API Keys**: Verify GROQ_API_KEY and TAVILY_API_KEY
3. **CORS**: Backend should allow frontend domain
4. **Environment Variables**: Ensure all required vars are set

### Debug Commands:
```bash
# Check backend logs
docker logs studybuddy-backend

# Test database connection
docker exec -it studybuddy-backend python -c "from studybuddy.database.connection import get_db; print('DB OK')"
```

---

## Production Checklist

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] SSL certificates (handled by Render/Streamlit)
- [ ] Domain names configured
- [ ] Monitoring set up
- [ ] Backup strategy implemented
- [ ] Performance testing completed
