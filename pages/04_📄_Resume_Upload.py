# In pages/04_Ã°Å¸â€œâ€ž_Resume_Upload.py

import streamlit as st
import requests
from studybuddy.tools.resume_parser import extract_text_from_upload

# Page config
st.set_page_config(
    page_title="Resume Upload - StudyBuddy AI",
    page_icon="Ã°Å¸â€œâ€ž",
    layout="wide"
)

# Get backend URL from session state
from frontend_config import get_backend_url
BACKEND_URL = get_backend_url()
UPLOAD_RESUME_URL = f"{BACKEND_URL}/api/upload-resume/"
GET_RESUME_SUMMARY_URL = f"{BACKEND_URL}/api/resume-summary/"

# Check authentication
if "access_token" not in st.session_state or not st.session_state.access_token:
    st.error("Ã°Å¸â€â€™ Please log in first from the Todo List page.")
    st.info("Go to the Todo List page to create an account or log in.")
    st.stop()

# Authorization header
auth_headers = {"Authorization": f"Bearer {st.session_state.access_token}"}

# Page title
st.title("Ã°Å¸â€œâ€ž Resume Upload & Analysis")
st.markdown("Upload your resume to get personalized interview questions based on your experience!")

# Fetch current resume summary if available
try:
    summary_response = requests.get(GET_RESUME_SUMMARY_URL, headers=auth_headers, timeout=10)
    if summary_response.status_code == 200:
        current_summary = summary_response.json().get("resume_summary", "")
        if current_summary:
            st.success("Ã¢Å“â€¦ You have a resume uploaded!")
            with st.expander("Ã°Å¸â€œâ€¹ View Current Resume Summary", expanded=False):
                st.markdown(current_summary)
except Exception as e:
    # User might not have a resume yet, that's okay
    pass

st.divider()

# Upload section
st.header("Ã°Å¸â€œÂ¤ Upload Your Resume")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Choose a PDF or text file",
        type=["pdf", "txt"],
        help="Upload your resume as a PDF or text file. The AI will analyze it and use it to personalize your interview questions."
    )

with col2:
    st.markdown("### Ã°Å¸â€œÂ Or Paste Text")
    paste_text = st.text_area(
        "Paste your resume text here",
        height=150,
        help="Alternatively, you can paste your resume text directly"
    )

# Process upload
if st.button("Ã°Å¸Å¡â‚¬ Upload & Analyze Resume", type="primary", use_container_width=True):
    resume_text = None
    
    # Get text from file or paste
    if uploaded_file is not None:
        with st.spinner("Ã°Å¸â€œâ€ž Extracting text from file..."):
            try:
                resume_text = extract_text_from_upload(uploaded_file)
                st.success(f"Ã¢Å“â€¦ Extracted {len(resume_text)} characters from {uploaded_file.name}")
            except Exception as e:
                st.error(f"Ã¢ÂÅ’ Failed to extract text: {str(e)}")
                st.stop()
    elif paste_text:
        resume_text = paste_text
        st.success(f"Ã¢Å“â€¦ Using pasted text ({len(resume_text)} characters)")
    else:
        st.warning("Ã¢Å¡Â Ã¯Â¸Â Please upload a file or paste your resume text.")
        st.stop()
    
    if resume_text:
        # Show preview
        with st.expander("Ã°Å¸â€˜â‚¬ Preview Resume Text", expanded=False):
            st.text(resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text)
        
        # Upload to backend
        with st.spinner("Ã°Å¸Â¤â€“ AI is analyzing your resume and generating a summary..."):
            try:
                payload = {"text_content": resume_text}
                response = requests.post(
                    UPLOAD_RESUME_URL,
                    json=payload,
                    headers=auth_headers,
                    timeout=120  # Resume processing might take a while
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("Ã¢Å“â€¦ Resume uploaded and analyzed successfully!")
                    
                    # Show summary
                    st.markdown("### Ã°Å¸â€œÅ  Resume Summary")
                    st.markdown(result.get("summary", ""))
                    
                    # Show RAG status
                    if result.get("rag_enabled", False):
                        st.info("Ã¢Å“Â¨ Your resume is now stored in the AI's memory for personalized interview questions!")
                    else:
                        st.warning("Ã¢Å¡Â Ã¯Â¸Â Resume summary saved, but vector storage may not be enabled.")
                    
                    st.balloons()
                    
                    # Refresh the page to show updated summary
                    st.rerun()
                else:
                    # Handle non-JSON errors gracefully (e.g., 502 Bad Gateway HTML from Render)
                    try:
                        error_json = response.json()
                        error_detail = error_json.get("detail", response.text)
                    except Exception:
                        error_detail = response.text or f"Status code: {response.status_code}"
                    st.error(f"Ã¢ÂÅ’ Failed to upload resume: {error_detail}")
                    
            except requests.exceptions.Timeout:
                st.error("Ã¢ÂÂ±Ã¯Â¸Â Request timed out. The resume might be too large. Try a shorter version.")
            except requests.exceptions.RequestException as e:
                st.error(f"Ã¢ÂÅ’ Error communicating with server: {str(e)}")
            except Exception as e:
                st.error(f"Ã¢ÂÅ’ Unexpected error: {str(e)}")

st.divider()

# Information section
st.markdown("### Ã°Å¸â€™Â¡ How It Works")
info_col1, info_col2, info_col3 = st.columns(3)

with info_col1:
    st.markdown("""
    **1. Upload Resume**
    - PDF or text format
    - AI extracts all text
    """)

with info_col2:
    st.markdown("""
    **2. AI Analysis**
    - Generates summary
    - Extracts key skills
    - Identifies experience
    """)

with info_col3:
    st.markdown("""
    **3. Personalized Prep**
    - Interview questions
    - Based on your resume
    - Context-aware responses
    """)

st.markdown("""
---
**Ã°Å¸â€™Â¡ Tip:** After uploading your resume, go to the Todo List page and click "Discuss" on any task to get personalized interview questions based on your actual experience!
""")




