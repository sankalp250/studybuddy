# In pages/04_👤_Account.py

import streamlit as st
import requests

st.set_page_config(page_title="My Account", page_icon="👤", layout="centered")

# --- API URLs ---
BASE_API_URL = "http://127.0.0.1:8000/api"
TOKEN_URL = f"{BASE_API_URL}/token"
USERS_URL = f"{BASE_API_URL}/users/"

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
                        response.raise_for_status() # Raise an error for bad responses
                        
                        token_data = response.json()
                        st.session_state.access_token = token_data["access_token"]
                        st.session_state.user_email = login_email
                        st.rerun() # Rerun the page to show the logged-in view

                    except requests.exceptions.HTTPError as e:
                        if e.response.status_code == 401:
                            st.error("Incorrect email or password.")
                        else:
                            st.error(f"Login failed. Server returned: {e.response.status_code}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection failed. Is the backend server running? Error: {e}")
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
                        response.raise_for_status()
                        
                        st.success("Account created successfully! Please go to the Login tab to sign in.")

                    except requests.exceptions.HTTPError as e:
                        try:
                            error_detail = e.response.json().get('detail', 'Unknown error')
                        except:
                            error_detail = f"HTTP {e.response.status_code}: {e.response.text}"
                        st.error(f"Sign up failed. Server returned: {error_detail}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection failed. Is the backend running? Error: {e}")
                else:
                    st.warning("Please enter both email and password.")