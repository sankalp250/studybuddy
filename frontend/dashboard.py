# In dashboard.py

import streamlit as st
import requests

# --- Page Configuration ---
# Set the page title and a descriptive icon
st.set_page_config(page_title="StudyBuddy AI", page_icon="🤖", layout="wide")

# --- Application Title and Description ---
st.title("🤖 StudyBuddy AI Daily Digest")
st.markdown("Your intelligent assistant to catch up on the latest news. Enter a topic, and I'll generate a summary for you using an advanced AI agent.")

# --- Backend API URL ---
# This is the endpoint of our FastAPI backend where the agent lives.
# Make sure your FastAPI server is running for this to work.
API_URL = "http://127.0.0.1:8000/api/daily-digest/"

# --- User Input Section ---
st.header("🔍 Get a News Summary")
# Create a text input box for the user's query.
user_query = st.text_input(
    label="Enter a topic you want to learn about:",
    value="Latest news on generative AI",
    help="For example: 'Latest breakthroughs in AI hardware' or 'Nvidia's new AI chips'"
)

# --- Generate Button and Output Area ---
if st.button("Generate Digest", type="primary"):
    # Ensure the user has entered a query
    if user_query:
        # --- Make the API Request to the Backend ---
        # Show a spinner while the agent is working in the background.
        with st.spinner("Hold on... The AI agent is searching and summarizing the web for you..."):
            try:
                # The data to send to the FastAPI endpoint (must match the DigestRequest schema)
                payload = {"query": user_query}
                
                # Make the POST request
                response = requests.post(API_URL, json=payload, timeout=180) # Set a longer timeout
                
                # Check if the request was successful
                response.raise_for_status()  # This will raise an error for bad responses (4xx or 5xx)
                
                # --- Display the Result ---
                result = response.json()
                st.subheader("📝 Here's Your AI-Generated Summary:")
                st.markdown(result.get("response", "No response found."))

            except requests.exceptions.RequestException as e:
                # Handle connection errors, timeouts, etc.
                st.error(f"Failed to connect to the backend API. Please make sure the backend server is running. Error: {e}")
            except Exception as e:
                # Handle other potential errors, including 500 from the server
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter a topic to generate a summary.")