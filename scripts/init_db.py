# In scripts/init_db.py

import sys
import os
import logging

# Add the parent directory to Python path so we can import studybuddy
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from studybuddy.database.connection import engine, Base
from studybuddy.database.models import User, StudyTopic  # Import all models
from studybuddy.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Debug: Print the database URL being used
logger.info("Database URL: %s", settings.DATABASE_URL)

def initialize_database():
    """
    Connects to the database and creates all tables
    based on the defined models.
    """
    try:
        logger.info("Connecting to the database...")
        # The magic happens here. SQLAlchemy creates the tables.
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
        logger.info("Current tables in metadata: %s", Base.metadata.tables.keys())
    except Exception as e:
        logger.error("An error occurred during database initialization: %s", e)
        raise

if __name__ == "__main__":
    initialize_database()