# In pages/04_👤_Account.py

import streamlit as st
import requests
import os

st.set_page_config(page_title="My Account", page_icon="👤", layout="centered")

# --- Get backend URL from session state or use fallback ---
BACKEND_BASE = st.session_state.get("backend_url", os.getenv("BACKEND_URL", "http://127.0.0.1:8000"))
BASE_API_URL = f"{BACKEND_BASE}/api"
TOKEN_URL = f"{BASE_API_URL}/token"
USERS_URL = f"{BASE_API_URL}/users/"

# Debug: Show which URL is being used
if "show_debug" not in st.session_state:
    st.session_state.show_debug = False

# Toggle for debugging
with st.sidebar:
    if st.checkbox("Show Debug Info"):
        st.session_state.show_debug = True
        st.info(f"Backend URL: {BACKEND_BASE}")
        st.info(f"API URL: {BASE_API_URL}")
        st.info(f"Token URL: {TOKEN_URL}")

# --- Initialize session state ---
# This is Streamlit's way of "remembering" things across reruns.
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# --- Main Page Logic ---

# If we have a token, the user is logged in.
if st.session_state.access_token:
    st.title(f"👋 Welcome, {st.session_state.user_email}!")
    st.markdown("You are now logged in.")
    
    # Resume Upload Section
    st.divider()
    st.header("📄 Upload Your Resume")
    st.markdown("Upload your resume to get personalized interview prep questions!")
    
    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'txt'])
    
    if uploaded_file is not None:
        if st.button("Upload & Process Resume"):
            with st.spinner("Processing your resume..."):
                try:
                    # Read the file content
                    file_content = uploaded_file.read()
                    
                    # Extract text based on file type
                    if uploaded_file.type == "application/pdf":
                        from studybuddy.tools.resume_parser import extract_text_from_pdf
                        resume_text = extract_text_from_pdf(file_content)
                    else:
                        resume_text = file_content.decode('utf-8')
                    
                    # Upload to backend
                    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
                    response = requests.post(
                        f"{BASE_API_URL}/upload-resume/",
                        json={"text_content": resume_text},
                        headers=headers,
                        timeout=60
                    )
                    response.raise_for_status()
                    
                    st.success("✅ Resume uploaded and processed successfully!")
                    result = response.json()
                    with st.expander("View Resume Summary"):
                        st.write(result.get("summary", ""))
                    
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 401:
                        st.error("Please login again. Your session may have expired.")
                        st.session_state.access_token = None
                        st.rerun()
                    else:
                        st.error(f"Server error: {e.response.text}")
                except Exception as e:
                    st.error(f"Failed to upload resume: {e}")
    
    # Get current resume summary
    st.divider()
    st.header("📋 Current Resume Summary")
    if st.button("Load Resume Summary"):
        try:
            headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
            response = requests.get(
                f"{BASE_API_URL}/resume-summary/",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            summary_data = response.json()
            summary_text = summary_data.get("resume_summary", "No resume uploaded yet.")
            st.info(summary_text)
            if summary_text != "No resume uploaded yet.":
                st.success("Resume summary loaded successfully!")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                st.error("Please login again. Your session may have expired.")
                st.session_state.access_token = None
                st.rerun()
            else:
                st.error(f"Could not load resume summary: {e}")
        except Exception as e:
            st.error(f"Could not load resume summary: {e}")

    if st.button("Logout"):
        # Clear the session state to log the user out
        st.session_state.access_token = None
        st.session_state.user_email = None
        st.rerun() # Rerun the page to show the logged-out view

else:
    # If no token, show Login / Sign Up options
    st.title("👤 Account Login / Sign Up")
    
    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    # --- Login Tab ---
    with login_tab:
        with st.form("login_form"):
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_password")
            login_button = st.form_submit_button("Login")

            if login_button:
                if login_email and login_password:
                    # The backend expects 'username' and 'password' in a form, not JSON
                    login_data = {
                        "username": login_email,
                        "password": login_password
                    }
                    try:
                        response = requests.post(TOKEN_URL, data=login_data, timeout=10)
                        
                        # Show detailed error information
                        if st.session_state.show_debug:
                            st.info(f"Response Status: {response.status_code}")
                            st.info(f"Response Text: {response.text}")
                        
                        response.raise_for_status() # Raise an error for bad responses
                        
                        token_data = response.json()
                        st.session_state.access_token = token_data["access_token"]
                        st.session_state.user_email = login_email
                        st.rerun() # Rerun the page to show the logged-in view

                    except requests.exceptions.HTTPError as e:
                        if e.response.status_code == 401:
                            st.error("Incorrect email or password.")
                        elif e.response.status_code == 500:
                            error_detail = e.response.text
                            st.error(f"Server error (500): {error_detail}")
                            if st.session_state.show_debug:
                                st.exception(e)
                        else:
                            st.error(f"Login failed. Server returned: {e.response.status_code}")
                            if st.session_state.show_debug:
                                st.text(f"Details: {e.response.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection failed. Is the backend server running? Error: {e}")
                        if st.session_state.show_debug:
                            st.exception(e)
                else:
                    st.warning("Please enter both email and password.")

    # --- Sign Up Tab ---
    with signup_tab:
        with st.form("signup_form"):
            signup_email = st.text_input("Email", key="signup_email")
            signup_password = st.text_input("Password", type="password", key="signup_password")
            signup_button = st.form_submit_button("Sign Up")

            if signup_button:
                if signup_email and signup_password:
                    signup_data = {
                        "email": signup_email,
                        "password": signup_password
                    }
                    try:
                        response = requests.post(USERS_URL, json=signup_data, timeout=10)
                        
                        # Show detailed error information
                        if st.session_state.show_debug:
                            st.info(f"Response Status: {response.status_code}")
                            st.info(f"Response Text: {response.text}")
                        
                        response.raise_for_status()
                        
                        st.success("Account created successfully! Please go to the Login tab to sign in.")

                    except requests.exceptions.HTTPError as e:
                        error_detail = "Unknown error"
                        try:
                            error_detail = e.response.json().get('detail', 'Unknown error')
                        except:
                            error_detail = f"HTTP {e.response.status_code}: {e.response.text}"
                        
                        if e.response.status_code == 500:
                            st.error(f"Sign up failed. Server returned: {error_detail}")
                            if st.session_state.show_debug:
                                st.exception(e)
                        elif e.response.status_code == 400:
                            st.error(f"Sign up failed: {error_detail}")
                        else:
                            st.error(f"Sign up failed. Server returned: {error_detail}")
                            if st.session_state.show_debug:
                                st.text(f"Details: {e.response.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection failed. Is the backend running? Error: {e}")
                        if st.session_state.show_debug:
                            st.exception(e)
                else:
                    st.warning("Please enter both email and password.")