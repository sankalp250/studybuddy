# In pages/01_🎯_Todo_List.py (INTERACTIVE VERSION)

import streamlit as st
import requests

# --- Page Configuration ---
st.set_page_config(page_title="My Smart TODOs", page_icon="🎯", layout="wide")

# --- Backend API URLs ---
BASE_API_URL = "http://127.0.0.1:8000/api"
USER_ID = 1
TODO_API_URL = f"{BASE_API_URL}/users/{USER_ID}/todos/"
DIGEST_API_URL = f"{BASE_API_URL}/daily-digest/"

# --- Page Title ---
st.title("🎯 My Smart TODO List")
st.markdown("Add and manage your study tasks. Click 'Prepare with AI' to get a head start!")

# --- Session State Initialization ---
# This helps us remember which to-do is being prepared.
if "selected_todo" not in st.session_state:
    st.session_state.selected_todo = None

# Callback function to set the selected to-do
def set_selected_todo(todo):
    st.session_state.selected_todo = todo

# --- Display the TODO List ---
try:
    response = requests.get(TODO_API_URL, timeout=10)
    response.raise_for_status()
    todos = response.json()

    if not todos:
        st.info("You have no tasks yet. Add one below!")
    else:
        st.write("Your current tasks:")
        # Sort todos to show active ones first
        todos.sort(key=lambda x: x.get('is_completed', False))
        
        for todo in todos:
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.checkbox(label=todo['title'], value=todo.get('is_completed', False), key=f"todo_{todo['id']}", disabled=True)
            with col2:
                # Add our "Prepare with AI" button for each to-do
                st.button("Prepare with AI ⚡", key=f"prepare_{todo['id']}", on_click=set_selected_todo, args=[todo])

except requests.exceptions.RequestException as e:
    st.error(f"Could not load TODOs. Is the backend server running? Error: {e}")

st.divider()

# --- Section to Display AI Preparation ---
if st.session_state.selected_todo:
    st.header(f"🧠 AI Preparation for: \"{st.session_state.selected_todo['title']}\"")
    
    # Use the title of the to-do as the query for our agent
    query = f"Generate a study guide for: {st.session_state.selected_todo['title']}. Include key topics, potential questions, and relevant resources."
    
    with st.spinner("🚀 Your AI study buddy is generating a personalized prep plan..."):
        try:
            payload = {"query": query}
            response = requests.post(DIGEST_API_URL, json=payload, timeout=180)
            response.raise_for_status()
            result = response.json()
            
            st.markdown(result.get("response", "No response found."))

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to generate study guide. Error: {e}")

st.divider()

# --- Form for adding a new TODO ---
with st.form(key="add_todo_form"):
    new_todo_title = st.text_input("Add a new task:", placeholder="e.g., Final exam for Advanced Algorithms")
    submit_button = st.form_submit_button(label="Add Task")

    if submit_button and new_todo_title:
        with st.spinner("Adding task..."):
            try:
                payload = {"title": new_todo_title}
                response = requests.post(TODO_API_URL, json=payload, timeout=10)
                response.raise_for_status()
                # Clear the selected to-do state to avoid confusion
                st.session_state.selected_todo = None
                # Rerun the script to refresh the list instantly
                st.rerun() 
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to add task. Error: {e}")