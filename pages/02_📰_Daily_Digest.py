# In pages/02_📰_Daily_Digest.py

import streamlit as st
import requests

# --- Page Configuration ---
st.set_page_config(page_title="AI Daily Digest", page_icon="📰", layout="wide")

# --- Authentication Check ---
if "access_token" not in st.session_state or st.session_state.access_token is None:
    st.error("🔒 Please log in to access the Daily Digest.")
    st.page_link("pages/04_👤_Account.py", label="Go to Account Page")
    st.stop()

# --- Backend API URLs ---
API_URL = "http://localhost:8000/api/daily-digest/"

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