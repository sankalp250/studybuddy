# In pages/01_🎯_Todo_List.py

import streamlit as st
import requests

# --- Page Configuration ---
# st.set_page_config(page_title="My Smart TODOs", page_icon="🎯", layout="centered") # <-- REMOVE THIS LINE

# --- Backend API URLs ---
BASE_API_URL = "http://127.0.0.1:8000/api"
USER_ID = 1  # Hardcoded for now
TODO_API_URL = f"{BASE_API_URL}/users/{USER_ID}/todos/"

# --- Page Title ---
st.title("🎯 My Smart TODO List")
st.markdown("Add and manage your study tasks. The AI will help you tackle these soon!")

# We use a placeholder that will be filled with the list of todos
todo_list_placeholder = st.empty()

def refresh_todo_list():
    """Fetches and displays the current list of TODOs."""
    try:
        response = requests.get(TODO_API_URL, timeout=10)
        response.raise_for_status()
        todos = response.json()
        
        with todo_list_placeholder.container():
            if not todos:
                st.info("You have no tasks yet. Add one below!")
            else:
                todos.sort(key=lambda x: x.get('is_completed', False))
                for todo in todos:
                    st.checkbox(label=todo['title'], value=todo.get('is_completed', False), key=f"todo_{todo['id']}", disabled=True)
    except requests.exceptions.RequestException as e:
        st.error(f"Could not load TODOs. Is the backend server running? Error: {e}")

# --- Form for adding a new TODO ---
with st.form(key="add_todo_form", clear_on_submit=True):
    new_todo_title = st.text_input("Add a new task:", placeholder="e.g., ML interview with Google on Friday")
    submit_button = st.form_submit_button(label="Add Task")

    if submit_button and new_todo_title:
        with st.spinner("Adding task..."):
            try:
                payload = {"title": new_todo_title}
                response = requests.post(TODO_API_URL, json=payload, timeout=10)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to add task. Error: {e}")

# --- Load the list ---
# We always call this to ensure the list is up-to-date after a form submission or page load
refresh_todo_list()