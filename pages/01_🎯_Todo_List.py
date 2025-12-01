# In pages/01_🎯_Todo_List.py (CONVERSATIONAL CHAT VERSION)

import streamlit as st
import requests
import os

# --- Page Config & URLs ---
st.set_page_config(page_title="My Smart TODOs", page_icon="🎯", layout="wide")

# --- Get backend URL from session state or use fallback ---
BASE_API_URL = st.session_state.get("backend_url", os.getenv("BACKEND_URL", "https://studybuddy-huu6.onrender.com"))
BASE_API_URL = f"{BASE_API_URL}/api"
TODO_API_URL = f"{BASE_API_URL}/todos/"  # Updated URL
AGENT_CHAT_URL = f"{BASE_API_URL}/agent/chat/"
TOKEN_URL = f"{BASE_API_URL}/token"
USERS_URL = f"{BASE_API_URL}/users/"

# If the user isn't logged in, don't show the page.
if "access_token" not in st.session_state or st.session_state.access_token is None:
    st.error("🔒 Authentication required.")
    with st.sidebar:
        st.subheader("Authentication")
        current_backend = st.session_state.get("backend_url", os.getenv("BACKEND_URL", "https://studybuddy-huu6.onrender.com"))
        new_backend = st.text_input("Backend URL", value=current_backend)
        if new_backend and new_backend != current_backend:
            st.session_state.backend_url = new_backend
            st.success("Backend URL updated.")

        # --- Quick Login ---
        st.markdown("### Login")
        login_email = st.text_input("Email", key="todo_login_email")
        login_password = st.text_input("Password", type="password", key="todo_login_password")
        if st.button("Login", use_container_width=True):
            if login_email and login_password:
                try:
                    data = {"username": login_email, "password": login_password}
                    resp = requests.post(TOKEN_URL, data=data, timeout=15)
                    resp.raise_for_status()
                    st.session_state.access_token = resp.json().get("access_token")
                    st.session_state.user_email = login_email
                    st.success("Logged in. Rerunning...")
                    st.rerun()
                except requests.exceptions.RequestException as e:
                    st.error(f"Login failed: {e}")
            else:
                st.warning("Enter email and password.")

        # --- Quick Sign Up ---
        st.markdown("### Sign Up")
        signup_email = st.text_input("New Email", key="todo_signup_email")
        signup_password = st.text_input("New Password", type="password", key="todo_signup_password")
        if st.button("Create Account", use_container_width=True):
            if signup_email and signup_password:
                try:
                    payload = {"email": signup_email, "password": signup_password}
                    resp = requests.post(USERS_URL, json=payload, timeout=15)
                    if resp.status_code == 201:
                        st.success("Account created. Use Login above.")
                    else:
                        try:
                            detail = resp.json().get("detail", resp.text)
                        except Exception:
                            detail = resp.text
                        st.error(f"Sign up failed: {detail}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Sign up failed: {e}")
            else:
                st.warning("Enter email and password.")

        st.markdown("### Or Paste Token")
        token_val = st.text_input("Access Token", type="password")
        if st.button("Set Token"):
            if token_val:
                st.session_state.access_token = token_val
                st.success("Token saved. Rerunning...")
                st.rerun()
            else:
                st.warning("Enter a token first.")
    st.stop()

# We need to create the authorization header
auth_headers = {"Authorization": f"Bearer {st.session_state.access_token}"}

# --- Page Title ---
st.title("🎯 My Smart TODO List")
st.markdown("Select a task to begin a dynamic, AI-powered interview prep session!")

# --- Session State for Chat History ---
# This is crucial for remembering the conversation
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "current_topic" not in st.session_state:
    st.session_state.current_topic = ""

# --- Layout: Two Columns ---
col1, col2 = st.columns([0.4, 0.6])

# --- Column 1: Task Management ---
with col1:
    st.header("Your Tasks")
    
    with st.form(key="add_todo_form"):
        new_todo_title = st.text_input("Add a new task:", placeholder="e.g., Convolutional Neural Networks")
        submit_button = st.form_submit_button(label="Add Task")

        if submit_button and new_todo_title:
            try:
                requests.post(TODO_API_URL, json={"title": new_todo_title}, headers=auth_headers, timeout=10).raise_for_status()
                st.rerun()
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to add task: {e}")
    st.divider()

    try:
        response = requests.get(TODO_API_URL, headers=auth_headers, timeout=10)
        response.raise_for_status()
        todos = response.json()
        
        if not todos:
            st.info("No tasks yet.")
        else:
            todos.sort(key=lambda x: x.get('is_completed', False))
            for todo in todos:
                # Callback function to start a chat session
                def start_chat_session(todo_title):
                    st.session_state.current_topic = todo_title
                    st.session_state.chat_messages = [{"role": "assistant", "content": f"Hello! Let's prepare for your task: **{todo_title}**. Ask me anything, or I can generate some initial questions for you."}]
                
                st.button(f"Discuss: {todo['title']} 🧠", key=f"prepare_{todo['id']}", on_click=start_chat_session, args=[todo['title']])
    except requests.exceptions.RequestException as e:
        st.error(f"Could not load TODOs: {e}")

# --- Column 2: Chat Interface ---

with col2:
    st.header("AI Prep Session")
    if st.session_state.current_topic:
        st.info(f"Currently discussing: **{st.session_state.current_topic}**")

        # --- NEW "Generate Flashcards" BUTTON ---
        if st.button("Create Flashcards from this Conversation 🪄"):
            with st.spinner("AI is analyzing the conversation to create flashcards..."):
                # Combine the conversation history into a single block of text
                conversation_text = "\n".join(
                    [f"{msg['role']}: {msg['content']}" for msg in st.session_state.chat_messages]
                )
                
                try:
                    headers = {"Authorization": f"Bearer {st.session_state.get('access_token')}"}
                    payload = {"text_content": conversation_text}
                    
                    response = requests.post(
                        f"{BASE_API_URL}/generate-flashcards/",
                        json=payload,
                        headers=headers,
                        timeout=180
                    )
                    response.raise_for_status()
                    
                    st.success(response.json().get("detail", "Flashcards created!"))
                    st.toast("✅ Flashcards saved! Check the SRS Review page later.")

                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to create flashcards. Error: {e}")

        # Display existing chat messages
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a follow-up question..."):
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Format chat messages for the API
                        api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_messages]
                        # Include study topic for RAG-based personalized questions
                        payload = {
                            "messages": api_messages,
                            "study_topic": st.session_state.current_topic or "Interview Preparation"
                        }
                        response = requests.post(AGENT_CHAT_URL, json=payload, headers=auth_headers, timeout=60)
                        response.raise_for_status()
                        ai_response = response.json()["response"]
                        st.markdown(ai_response)
                        st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})
                    except requests.exceptions.RequestException as e:
                        error_msg = f"Error communicating with the agent: {e}"
                        st.error(error_msg)
                        st.session_state.chat_messages.append({"role": "assistant", "content": error_msg})
    else:
        st.info("👈 Select a task from the left to start preparing!")