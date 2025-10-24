# In pages/04_💻_LeetCode_Practice.py (MULTI-PROBLEM VERSION)

import streamlit as st
import requests
import time

st.set_page_config(page_title="LeetCode Practice", page_icon="💻", layout="wide")

API_URL = "http://127.0.0.1:8000/api/generate-leetcode/"

st.title("💻 Brain-Sharp LeetCode Generator")
st.markdown("Generate a set of AI-created coding problems to sharpen your skills.")

# Use a list to store multiple problems
if "leetcode_problems" not in st.session_state:
    st.session_state.leetcode_problems = []

# --- Layout for user inputs ---
col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("Enter a topic:", "Graphs and Trees")
with col2:
    difficulty = st.selectbox("Select a difficulty:", ["Easy", "Medium", "Hard"])

# --- Generate button and logic ---
if st.button("Generate Problem Set (3 Questions)", type="primary"):
    # Clear old problems
    st.session_state.leetcode_problems = []
    
    # We will show a progress bar as we generate the questions one by one
    progress_bar = st.progress(0.0, text="Initializing...")
    
    # Loop 3 times to generate 3 problems
    for i in range(3):
        progress_text = f"🧠 AI is crafting problem {i + 1} of 3..."
        progress_bar.progress((i) / 3.0, text=progress_text)
        
        try:
            payload = {"topic": topic, "difficulty": difficulty}
            response = requests.post(API_URL, json=payload, timeout=180)
            response.raise_for_status()
            
            result = response.json()
            problem = result.get("response")
            if problem:
                st.session_state.leetcode_problems.append(problem)
            
            # Add a small delay to avoid overwhelming the API and to show progress
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to generate problem {i + 1}. Is the backend running? Error: {e}")
            break # Stop if one of the API calls fails
            
    progress_bar.progress(1.0, text="✅ Problem set generated!")
    time.sleep(1)
    progress_bar.empty()


# --- Display the problems ---
if st.session_state.leetcode_problems:
    st.divider()
    st.header("Your AI-Generated Problem Set:")
    
    for i, problem in enumerate(st.session_state.leetcode_problems):
        st.subheader(f"Problem #{i + 1}")
        st.markdown(problem, unsafe_allow_html=True)
        st.divider()