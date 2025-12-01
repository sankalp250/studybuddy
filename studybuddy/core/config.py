# In studybuddy/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

    DATABASE_URL: str

# Create a single, globally accessible instance of the Settings object.
settings = Settings()