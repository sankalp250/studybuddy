# In dashboard.py (the main home page)

import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="StudyBuddy AI - Home",
    page_icon="🤖",
    layout="wide"
)

# Welcome Message
st.title("Welcome to StudyBuddy AI! 🤖")
st.markdown("Your intelligent ecosystem for focused learning and interview preparation.")
st.info("Select a tool from the sidebar on the left to get started.")

st.divider()

# How-to Guide or Feature Showcase
st.header("What can StudyBuddy do for you?")
st.markdown("""
- **🎯 Smart TODO List:** Keep track of your study goals and deadlines. Our AI will soon help you prepare for them automatically.
- **📰 AI-Powered Daily Digest:** Don't have time to keep up with the news? Get concise, AI-generated summaries on any topic.
""")