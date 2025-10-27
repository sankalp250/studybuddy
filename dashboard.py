# In dashboard.py (FINAL VERSION)

import streamlit as st
import os
import requests

st.set_page_config(
    page_title="StudyBuddy AI - Home",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get backend URL with fallback for local development
try:
    # Try to get from Streamlit secrets (for deployment)
    BACKEND_URL = st.secrets.get("BACKEND_URL")
except:
    BACKEND_URL = None

# Fallback to environment variable or localhost
if not BACKEND_URL:
    BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Store in session state for use in pages
st.session_state.backend_url = BACKEND_URL

BASE_URL = BACKEND_URL

# Check backend connection status
@st.cache_data(ttl=10)  # Cache for 10 seconds
def check_backend_status(url):
    """Check if backend is running."""
    try:
        response = requests.get(url, timeout=3)
        return response.status_code == 200, response.json()
    except:
        return False, None

# Main layout
st.title("Welcome to StudyBuddy AI! 🤖")
st.markdown("Your intelligent ecosystem for focused learning and interview preparation.")

# Backend status indicator
st.divider()
backend_status, backend_data = check_backend_status(BACKEND_URL)

if backend_status:
    st.success(f"✅ Backend is running at {BACKEND_URL}")
    if backend_data:
        st.json(backend_data)
else:
    st.error(f"❌ Backend connection failed at {BACKEND_URL}")
    with st.expander("How to fix this"):
        st.markdown("""
        **To start your backend:**
        
        1. **Using Docker:**
           ```bash
           docker-compose up backend
           ```
        
        2. **Manual start:**
           ```bash
           uvicorn main:app --host 127.0.0.1 --port 8000 --reload
           ```
        
        3. **Check connection:**
           ```bash
           python scripts/test_backend_connection.py
           ```
        """)
    if st.button("🔄 Retry Connection", type="primary"):
        st.rerun()

st.divider()

# Features section
col1, col2, col3 = st.columns(3)

with col1:
    st.header("🎯 Smart TODO List")
    st.markdown("""
    - Track your study goals
    - Set deadlines and priorities
    - AI-powered interview prep
    - Personalized practice questions
    """)

with col2:
    st.header("📰 Daily Digest")
    st.markdown("""
    - AI-generated news summaries
    - Stay updated on any topic
    - Web-powered research
    - Concise, actionable insights
    """)

with col3:
    st.header("💻 LeetCode Practice")
    st.markdown("""
    - AI-generated coding problems
    - Multiple difficulty levels
    - Topic-focused practice
    - Interview-ready preparation
    """)

st.divider()

# Quick stats section
st.header("🚀 Features Overview")

feature_col1, feature_col2 = st.columns(2)

with feature_col1:
    st.markdown("""
    ### 📚 Study Tools
    - **Flashcard System with SRS**: Spaced repetition for efficient learning
    - **Resume-based Interview Prep**: Upload your resume for personalized questions
    - **Dynamic Chat Interface**: Interactive AI assistant for study sessions
    """)

with feature_col2:
    st.markdown("""
    ### 🤖 AI-Powered
    - **Groq LLM Integration**: Fast, efficient AI responses
    - **Tavily Web Search**: Real-time web research capabilities
    - **Context-Aware Assistance**: Personalized based on your profile
    """)

# Documentation links
st.divider()
st.markdown("### 📖 Quick Links")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 View API Docs", use_container_width=True):
        st.markdown(f"Visit: [{BACKEND_URL}/docs]({BACKEND_URL}/docs)")
