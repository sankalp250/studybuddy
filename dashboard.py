import streamlit as st
import os
import requests
import time
from frontend_config import get_backend_url, LIVE_RENDER_URL

st.set_page_config(
    page_title="StudyBuddy AI - Home",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Backend URL Resolution
# ---------------------------------------------------------
LOCAL_URL = "http://127.0.0.1:8000"
BACKEND_URL = get_backend_url()
BASE_URL = BACKEND_URL

# ---------------------------------------------------------
# Sidebar: Backend Server Settings
# ---------------------------------------------------------
with st.sidebar:
    st.subheader("âš™ï¸ Server Settings")
    st.markdown(f"**Current Backend:**\n{BACKEND_URL}")
    
    col_cloud, col_local = st.columns(2)
    with col_cloud:
        if st.button("🌐 Live Render", use_container_width=True):
            st.session_state.backend_url = LIVE_RENDER_URL
            st.rerun()
    with col_local:
        if st.button("💻 Localhost", use_container_width=True):
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
    st.error(f"âŒ Backend connection failed at {BACKEND_URL}")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        if "onrender.com" in BACKEND_URL:
            if st.button("⚡ Wake Up Render Backend", type="primary", use_container_width=True):
                with st.spinner("Pinging Render backend to wake up from free-tier sleep mode (takes ~30s)..."):
                    wake_success = False
                    start_time = time.time()
                    while time.time() - start_time < 50:
                        try:
                            r = requests.get(BACKEND_URL, timeout=8)
                            if r.status_code == 200:
                                wake_success = True
                                break
                        except Exception:
                            pass
                        time.sleep(3)
                        
                    if wake_success:
                        st.success("🎉 Backend is awake and ready!")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("Backend wake-up timed out. If this URL is inactive, try switching to https://studybuddy-huu6.onrender.com.")
        else:
            if st.button("🔄 Retry Connection", type="primary", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
                
    with col2:
        with st.expander("â„¹ï¸ Connection Tips"):
            st.markdown(f"""
            - **Active Production Backend**: The working Render backend for this app is:
              https://studybuddy-huu6.onrender.com
            - **Render Sleep Mode**: Render free instances spin down after 15 minutes of inactivity and wake up when pinged.
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

