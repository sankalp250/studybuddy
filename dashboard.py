import streamlit as st
import os
import requests
import time

st.set_page_config(
    page_title="StudyBuddy AI - Home",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Backend URL Resolution
# ---------------------------------------------------------
# 1. Environment variable (BACKEND_URL or BACKEND_API_URL)
# 2. Streamlit Cloud Secrets (if deployed on Streamlit Cloud)
# 3. Default to the production Render URL
CLOUD_RENDER_URL = "https://studybuddy-huu6.onrender.com"
LOCAL_URL = "http://127.0.0.1:8000"

env_backend = (
    os.getenv("BACKEND_URL")
    or os.getenv("BACKEND_API_URL")
    or (st.secrets.get("BACKEND_URL") if hasattr(st, "secrets") and "BACKEND_URL" in st.secrets else None)
)

default_target = env_backend.rstrip("/") if env_backend else CLOUD_RENDER_URL

if "backend_url" not in st.session_state:
    st.session_state.backend_url = default_target
elif st.session_state.backend_url in ("http://127.0.0.1:8000", "http://localhost:8000") and not env_backend:
    # Reset stale localhost default if no explicit local env var is set
    st.session_state.backend_url = CLOUD_RENDER_URL

BACKEND_URL = st.session_state.backend_url.rstrip("/")
st.session_state.backend_url = BACKEND_URL
BASE_URL = BACKEND_URL

# ---------------------------------------------------------
# Sidebar: Backend Server Settings
# ---------------------------------------------------------
with st.sidebar:
    st.subheader("⚙️ Server Settings")
    st.markdown(f"**Current Backend:**\n{BACKEND_URL}")
    
    col_cloud, col_local = st.columns(2)
    with col_cloud:
        if st.button("🌐 Use Render", use_container_width=True):
            st.session_state.backend_url = CLOUD_RENDER_URL
            st.rerun()
    with col_local:
        if st.button("💻 Use Local", use_container_width=True):
            st.session_state.backend_url = LOCAL_URL
            st.rerun()
            
    custom_url = st.text_input("Custom Backend URL", value=BACKEND_URL, key="custom_backend_input")
    if custom_url and custom_url.rstrip("/") != BACKEND_URL:
        if st.button("Apply URL", use_container_width=True):
            st.session_state.backend_url = custom_url.rstrip("/")
            st.rerun()

# ---------------------------------------------------------
# Health Check Logic
# ---------------------------------------------------------
@st.cache_data(ttl=15)
def check_backend_status(url, timeout=5):
    """Check if backend is reachable."""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, str(e)

# Main layout
st.title("Welcome to StudyBuddy AI! 🤖")
st.markdown("Your intelligent ecosystem for focused learning and interview preparation.")

st.divider()

# Check backend status
backend_status, backend_data = check_backend_status(BACKEND_URL, timeout=5)

if backend_status:
    st.success(f"✅ Backend is running and connected at **{BACKEND_URL}**")
    if isinstance(backend_data, dict):
        st.json(backend_data)
else:
    st.error(f"❌ Backend connection failed at {BACKEND_URL}")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        # Render Free Tier Wake Up Button
        if "onrender.com" in BACKEND_URL:
            if st.button("⚡ Wake Up Render Backend", type="primary", use_container_width=True):
                with st.spinner("Waking up Render backend... Free instances sleep after inactivity and can take 30-45 seconds to spin up."):
                    wake_success = False
                    start_time = time.time()
                    while time.time() - start_time < 50:
                        try:
                            r = requests.get(BACKEND_URL, timeout=10)
                            if r.status_code == 200:
                                wake_success = True
                                break
                        except Exception:
                            pass
                        time.sleep(4)
                        
                    if wake_success:
                        st.success("🎉 Backend is awake and ready!")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("Backend wake-up timed out. Please check your Render dashboard service status.")
        else:
            if st.button("🔄 Retry Connection", type="primary", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
                
    with col2:
        with st.expander("ℹ️ Why is this happening?"):
            st.markdown("""
            - **Render Free Tier Sleep Mode**: If you are connecting to Render (*.onrender.com), instances automatically spin down after 15 minutes of inactivity. Click **'Wake Up Render Backend'** above and wait ~30-45 seconds.
            - **Localhost Development**: If running locally, make sure your FastAPI backend is running via uvicorn main:app --host 127.0.0.1 --port 8000 --reload.
            - **Switch Server**: You can switch between Render Cloud and Localhost using the sidebar options.
            """)

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
st.markdown("### 🔗 Quick Links")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📖 View API Docs", use_container_width=True):
        st.markdown(f"Visit: [{BACKEND_URL}/docs]({BACKEND_URL}/docs)")
