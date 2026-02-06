import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analytics - StudyBuddy", page_icon="📊", layout="wide")

st.title("📊 Study Analytics")
st.markdown("Track your learning progress and habits.")

# Get backend URL
BASE_API_URL = st.session_state.get("backend_url", os.getenv("BACKEND_URL", "https://studybuddy-huu6.onrender.com"))
API_URL = f"{BASE_API_URL}/api/users/me/stats"

# Check authentication
if "access_token" not in st.session_state or not st.session_state.access_token:
    st.warning("🔒 Please log in to view your analytics.")
    st.info("You can log in from the 'Home' page or any other tool page.")
else:
    auth_headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    
    try:
        with st.spinner("Fetching your statistics..."):
            response = requests.get(API_URL, headers=auth_headers)
            
        if response.status_code == 200:
            stats = response.json()
            
            # Top Level Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Cards Reviewed", stats.get("total_cards_reviewed", 0))
            with col2:
                st.metric("Total Flashcards", stats.get("total_flashcards", 0))
            with col3:
                st.metric("Completed Todos", stats.get("completed_todos", 0))
            with col4:
                st.metric("Est. Study Hours", f"{stats.get('total_study_hours', 0)}h", help="Estimated based on 3 mins per review")

            st.divider()
            
            # Simple Chart: Activity Distribution
            # We don't have time-series data yet, so let's show distribution of work
            data = {
                "metric": ["Reviews", "Created Cards", "Completed Todos"],
                "count": [stats.get("total_cards_reviewed", 0), stats.get("total_flashcards", 0), stats.get("completed_todos", 0)]
            }
            df = pd.DataFrame(data)
            
            if df['count'].sum() > 0:
                st.subheader("Activity Overview")
                fig = px.bar(df, x="metric", y="count", title="Your Study Activity Stats", template="plotly_dark", color="metric")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Start using the app to see your activity stats here!")
        
        elif response.status_code == 401:
            st.warning("⚠️ Session expired or invalid. Please log in again.")
            if st.button("Refresh Login"):
                if "access_token" in st.session_state:
                    del st.session_state.access_token
                st.rerun()
                
        else:
            st.error(f"Failed to fetch analytics. Status: {response.status_code}. Detail: {response.text}")
            
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
