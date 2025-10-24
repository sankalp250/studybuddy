# In pages/03_🎬_YouTube_Summarizer.py

import streamlit as st
import requests

st.set_page_config(page_title="YouTube Summarizer", page_icon="🎬", layout="wide")

API_URL = "http://127.0.0.1:8000/api/summarize-youtube/"

st.title("🎬 YouTube Video Summarizer")
st.markdown("Paste the URL of any YouTube video with English captions, and the AI will generate a summary for you.")

# Use session state to remember the last summary
if "youtube_summary" not in st.session_state:
    st.session_state.youtube_summary = ""

# --- Form for user input ---
with st.form(key="youtube_form"):
    youtube_url = st.text_input(label="Enter a YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")
    submit_button = st.form_submit_button(label="Summarize Video")

    if submit_button:
        if youtube_url:
            with st.spinner("Hold on... The AI is fetching the transcript and generating your summary..."):
                try:
                    payload = {"url": youtube_url}
                    response = requests.post(API_URL, json=payload, timeout=180)
                    response.raise_for_status() # Raises an error for bad status codes
                    
                    result = response.json()
                    st.session_state.youtube_summary = result.get("response", "No summary could be generated.")
                
                except requests.exceptions.HTTPError as http_err:
                    try:
                        error_detail = http_err.response.json().get("detail", "An unknown error occurred.")
                        st.error(f"Error: {error_detail}")
                    except:
                        st.error(f"An HTTP error occurred: {http_err.response.status_code} {http_err.response.reason}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to connect to the backend. Is it running? Error: {e}")
        else:
            st.warning("Please enter a YouTube URL.")

# --- Display the summary outside the form ---
if st.session_state.youtube_summary:
    st.divider()
    st.subheader("📝 Your AI-Generated Summary:")
    st.markdown(st.session_state.youtube_summary)