# In pages/06_🧠_SRS_Review.py

import streamlit as st
import requests
import os

# --- Page Config & URLs ---
st.set_page_config(page_title="SRS Review", page_icon="🧠", layout="centered")

# --- Get backend URL from session state or use fallback ---
BASE_API_URL = st.session_state.get("backend_url", os.getenv("BACKEND_URL", "http://127.0.0.1:8000"))
BASE_API_URL = f"{BASE_API_URL}/api"
DUE_CARDS_URL = f"{BASE_API_URL}/flashcards/due/"

# --- Helper functions for API calls ---
def get_due_cards(headers):
    """Fetches a list of flashcards due for review."""
    try:
        response = requests.get(DUE_CARDS_URL, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to load review session: {e}")
        return []

def review_card(card_id, rating, headers):
    """Submits a review for a single flashcard."""
    review_url = f"{BASE_API_URL}/flashcards/{card_id}/review/"
    try:
        response = requests.post(review_url, json={"performance_rating": rating}, headers=headers, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to save review: {e}")
        return False

# --- Initialize Session State ---
# This is crucial for managing the review session flow
if 'due_cards' not in st.session_state:
    st.session_state.due_cards = []
if 'card_index' not in st.session_state:
    st.session_state.card_index = 0
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

# --- Main Page Logic ---
st.title("🧠 Spaced Repetition Review")

# Check for login first
if "access_token" not in st.session_state or st.session_state.access_token is None:
    st.error("🔒 Authentication required.")
    with st.sidebar:
        st.subheader("Authentication")
        # Allow setting backend URL
        current_backend = st.session_state.get("backend_url", os.getenv("BACKEND_URL", "http://127.0.0.1:8000"))
        new_backend = st.text_input("Backend URL", value=current_backend)
        if new_backend and new_backend != current_backend:
            st.session_state.backend_url = new_backend
            st.success("Backend URL updated.")
        # Allow pasting an existing token
        token_val = st.text_input("Paste Access Token", type="password")
        if st.button("Set Token"):
            if token_val:
                st.session_state.access_token = token_val
                st.success("Token saved. Rerunning...")
                st.rerun()
            else:
                st.warning("Enter a token first.")
else:
    auth_headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    
    # Load the review session if it hasn't been loaded yet
    if not st.session_state.due_cards:
        if st.button("Start Review Session", type="primary"):
            with st.spinner("Fetching cards due for review..."):
                st.session_state.due_cards = get_due_cards(auth_headers)
                st.session_state.card_index = 0
                st.session_state.show_answer = False
                st.rerun() # Rerun to start the session immediately

    # --- Review Session In Progress ---
    if st.session_state.due_cards:
        total_cards = len(st.session_state.due_cards)
        
        # Check if the session is complete
        if st.session_state.card_index >= total_cards:
            st.success("🎉 Review session complete! Great job!")
            st.balloons()
            # Clear the session data for the next time
            st.session_state.due_cards = []
            st.session_state.card_index = 0
            st.session_state.show_answer = False
            
        else:
            current_card = st.session_state.due_cards[st.session_state.card_index]
            progress = (st.session_state.card_index + 1) / total_cards
            st.progress(progress, text=f"Card {st.session_state.card_index + 1} of {total_cards}")

            # Display the current flashcard question
            st.subheader("Question:")
            st.markdown(f"> {current_card['question']}")
            
            st.divider()

            if not st.session_state.show_answer:
                if st.button("Show Answer", type="primary"):
                    st.session_state.show_answer = True
                    st.rerun()
            else:
                st.subheader("Answer:")
                st.markdown(current_card['answer'])

                # Performance rating buttons
                st.write("**How well did you recall this?**")
                col1, col2, col3 = st.columns(3)

                def handle_review(rating):
                    if review_card(current_card['id'], rating, auth_headers):
                        st.session_state.card_index += 1
                        st.session_state.show_answer = False
                        st.rerun()

                with col1:
                    st.button("Hard / Again (1)", on_click=handle_review, args=[1], use_container_width=True)
                with col2:
                    st.button("Good (3)", on_click=handle_review, args=[3], use_container_width=True)
                with col3:
                    st.button("Easy (5)", type="primary", on_click=handle_review, args=[5], use_container_width=True)

    else:
        st.info("You have no cards due for review right now. Come back later!")