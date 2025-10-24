# In studybuddy/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Manages application settings and loads environment variables.
    """
    # Load settings from a .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    # LLM API Keys
    GEMINI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    TAVILY_API_KEY: str | None = None

    # Database URL
    DATABASE_URL: str

# Create a single, globally accessible instance of the Settings object.
settings = Settings()