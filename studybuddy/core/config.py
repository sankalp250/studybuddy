from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GEMINI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    TAVILY_API_KEY: str | None = None
    DATABASE_URL: str | None = None
    GROQ_MODEL: str = "openai/gpt-oss-20b"

settings = Settings()

LIVE_RENDER_URL = "https://studybuddy-huu6.onrender.com"
DEFUNCT_RENDER_URL = "studybuddy-backend-xodg.onrender.com"

def get_backend_url() -> str:
    """
    Returns the active backend URL, automatically overriding any defunct URLs.
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

