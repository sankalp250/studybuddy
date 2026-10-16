import os

LIVE_RENDER_URL = "https://studybuddy-huu6.onrender.com"
DEFUNCT_RENDER_URL = "studybuddy-backend-xodg.onrender.com"

def get_backend_url() -> str:
    """
    Returns the active live backend URL, completely safe for frontend Streamlit Cloud.
    Requires NO database or pydantic dependencies.
    """
    try:
        import streamlit as st
        cached = st.session_state.get("backend_url")
        if cached and DEFUNCT_RENDER_URL not in cached:
            return cached.rstrip("/")

        env_val = (
            os.getenv("BACKEND_URL")
            or os.getenv("BACKEND_API_URL")
            or (st.secrets.get("BACKEND_URL") if hasattr(st, "secrets") and "BACKEND_URL" in st.secrets else None)
            or (st.secrets.get("BACKEND_API_URL") if hasattr(st, "secrets") and "BACKEND_API_URL" in st.secrets else None)
        )
        if env_val and DEFUNCT_RENDER_URL not in env_val and "127.0.0.1" not in env_val and "localhost" not in env_val:
            target = env_val.rstrip("/")
        else:
            target = LIVE_RENDER_URL

        st.session_state.backend_url = target
        return target
    except Exception:
        return LIVE_RENDER_URL
