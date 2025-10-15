# In studybuddy/database/models.py

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from .connection import Base

class User(Base):
    """
    Represents a user in the database.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class StudyTopic(Base):
    """
    Represents a topic a user wants to study for an interview.
    e.g., "Machine Learning Interview"
    """
    __tablename__ = "study_topics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    
    # TODO: Add a relationship to the User model later
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())