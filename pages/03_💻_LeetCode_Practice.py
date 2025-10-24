import streamlit as st
import requests

st.set_page_config(page_title="LeetCode Practice", page_icon="💻", layout="wide")

API_URL = "http://127.0.0.1:8000/api/generate-leetcode/"

st.title("💻 Brain-Sharp LeetCode Generator")
st.markdown("Generate an original, AI-created coding problem to sharpen your skills.")

# --- Session state to hold the generated problem ---
if "leetcode_problem" not in st.session_state:
    st.session_state.leetcode_problem = ""

# --- Layout for user inputs ---
col1, col2 = st.columns(2)

with col1:
    topic = st.text_input("Enter a topic:", "Dynamic Programming")

with col2:
    difficulty = st.selectbox("Select a difficulty:", ["Easy", "Medium", "Hard"])

# --- Generate button and logic ---
if st.button("Generate Problem", type="primary"):
    with st.spinner("🧠 The AI is crafting a new problem for you..."):
        try:
            payload = {"topic": topic, "difficulty": difficulty}
            response = requests.post(API_URL, json=payload, timeout=180)
            response.raise_for_status()
            
            result = response.json()
            st.session_state.leetcode_problem = result.get("response", "Could not generate a problem.")

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to generate problem. Is the backend running? Error: {e}")

# --- Display the problem outside the button's scope ---
if st.session_state.leetcode_problem:
    st.divider()
    st.markdown(st.session_state.leetcode_problem, unsafe_allow_html=True)
    # The 'unsafe_allow_html=True' is needed to render the <details> HTML tag correctly.
