# In studybuddy/database/models.py

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .connection import Base

class User(Base):
    """Represents a user in the database."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # This creates a back-reference from the User model to the Todo model
    todos = relationship("Todo", back_populates="owner")

class StudyTopic(Base):
    """Represents a topic a user wants to study for an interview."""
    __tablename__ = "study_topics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
# <<< --- NEW CODE STARTS HERE --- >>>

class Todo(Base):
    """Represents a to-do item in the database."""
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    is_completed = Column(Boolean, default=False)
    
    # This is the link to the user table. Each to-do must have an owner.
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # This creates the relationship so we can easily access the user from a to-do item
    owner = relationship("User", back_populates="todos")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

# <<< --- NEW CODE ENDS HERE --- >>>