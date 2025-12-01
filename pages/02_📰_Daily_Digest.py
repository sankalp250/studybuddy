# In pages/02_📰_Daily_Digest.py

import streamlit as st
import requests
import os

# --- Page Configuration ---
st.set_page_config(page_title="AI Daily Digest", page_icon="📰", layout="wide")

# --- Authentication Check ---
if "access_token" not in st.session_state or st.session_state.access_token is None:
    st.error("🔒 Authentication required.")
    with st.sidebar:
        st.subheader("Authentication")
        current_backend = st.session_state.get("backend_url", os.getenv("BACKEND_URL", "https://studybuddy-huu6.onrender.com"))
        new_backend = st.text_input("Backend URL", value=current_backend)
        if new_backend and new_backend != current_backend:
            st.session_state.backend_url = new_backend
            st.success("Backend URL updated.")
        token_val = st.text_input("Paste Access Token", type="password")
        if st.button("Set Token"):
            if token_val:
                st.session_state.access_token = token_val
                st.success("Token saved. Rerunning...")
                st.rerun()
            else:
                st.warning("Enter a token first.")
    st.stop()

# --- Get backend URL from session state or use fallback ---
BASE_API_URL = st.session_state.get("backend_url", os.getenv("BACKEND_URL", "https://studybuddy-huu6.onrender.com"))
BASE_API_URL = f"{BASE_API_URL}/api"
API_URL = f"{BASE_API_URL}/daily-digest/"

# --- Page Title & Description ---
st.title("📰 AI-Powered Daily Digest")
st.markdown("Enter any topic, and our advanced AI agent will search the web and generate a concise summary for you.")

# --- User Input Section ---
user_query = st.text_input(
    label="Enter a topic you want a summary on:",
    value="Latest breakthroughs in AI hardware"
)

# --- Generate Button and Output Area ---
if st.button("Generate Digest", type="primary"):
    if user_query:
        with st.spinner("Hold on... The AI agent is searching the web for you... This may take a moment."):
            try:
                payload = {"query": user_query}
                auth_headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
                response = requests.post(API_URL, json=payload, headers=auth_headers, timeout=180)
                response.raise_for_status()
                result = response.json()
                st.subheader("📝 Here's Your AI-Generated Summary:")
                st.markdown(result.get("response", "No response found."))
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the backend. Error: {e}")