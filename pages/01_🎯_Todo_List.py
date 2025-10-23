# In pages/01_🎯_Todo_List.py (IMPROVED UI/UX VERSION)

import streamlit as st
import requests

# --- Page Configuration & API URLs ---
st.set_page_config(page_title="My Smart TODOs", page_icon="🎯", layout="wide")
BASE_API_URL = "http://127.0.0.1:8000/api"
USER_ID = 1
TODO_API_URL = f"{BASE_API_URL}/users/{USER_ID}/todos/"
DIGEST_API_URL = f"{BASE_API_URL}/daily-digest/"

# --- Page Title ---
st.title("🎯 My Smart TODO List")
st.markdown("Add your study goals. Click **'Generate Study Questions'** to get a focused list of topics and questions.")

# --- Session State Initialization ---
if "prep_content" not in st.session_state:
    st.session_state.prep_content = ""
if "prep_title" not in st.session_state:
    st.session_state.prep_title = ""

def generate_prep_material(todo):
    """Callback function to trigger AI preparation."""
    st.session_state.prep_title = todo['title']
    st.session_state.prep_content = "" # Clear previous content

    # --- THIS IS OUR NEW, MORE FOCUSED PROMPT ---
    prompt = (
        f"I have an upcoming machine learning interview focused on '{todo['title']}'. "
        "Your task is to act as an expert technical interviewer. "
        "Generate 5 specific, in-depth interview questions that a top tech company might ask about this topic. "
        "For each question, provide a concise, high-quality answer. Structure the output clearly."
    )
    
    with st.spinner("🚀 Your AI study buddy is generating interview questions..."):
        try:
            payload = {"query": prompt}
            response = requests.post(DIGEST_API_URL, json=payload, timeout=180)
            response.raise_for_status()
            result = response.json()
            st.session_state.prep_content = result.get("response", "Could not generate content.")
        except requests.exceptions.RequestException as e:
            st.session_state.prep_content = f"Failed to generate study guide. Is the backend running? Error: {e}"

# --- Main Page Layout ---
# Use columns for a cleaner layout
col1, col2 = st.columns([1, 1]) # Split the page into two halves

with col1:
    st.header("Your Tasks")
    
    # --- Form for adding a new TODO ---
    with st.form(key="add_todo_form"):
        new_todo_title = st.text_input("Add a new task:", placeholder="e.g., Deep Learning Fundamentals")
        submit_button = st.form_submit_button(label="Add Task")

        if submit_button and new_todo_title:
            try:
                payload = {"title": new_todo_title}
                requests.post(TODO_API_URL, json=payload, timeout=10).raise_for_status()
                # Clear generated content when a new item is added
                st.session_state.prep_title = ""
                st.session_state.prep_content = ""
                st.rerun() # Use rerun to force a clean refresh of the list
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to add task. Error: {e}")
    
    st.divider()

    # --- Display the TODO List ---
    try:
        response = requests.get(TODO_API_URL, timeout=10)
        response.raise_for_status()
        todos = response.json()
        
        if not todos:
            st.info("You have no tasks yet.")
        else:
            todos.sort(key=lambda x: x.get('is_completed', False))
            for todo in todos:
                c1, c2 = st.columns([0.8, 0.2])
                c1.checkbox(label=todo['title'], value=todo.get('is_completed', False), key=f"todo_{todo['id']}", disabled=True)
                c2.button("Generate Study Questions 🧠", key=f"prepare_{todo['id']}", on_click=generate_prep_material, args=[todo])

    except requests.exceptions.RequestException as e:
        st.error(f"Could not load TODOs. Error: {e}")

with col2:
    st.header("AI Preparation Area")
    if st.session_state.prep_title:
        st.subheader(f"Generated Questions for: \"{st.session_state.prep_title}\"")
        st.markdown(st.session_state.prep_content)
    else:
        st.info("Click 'Generate Study Questions' on a task to see AI-generated material here.")