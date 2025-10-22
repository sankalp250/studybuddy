# In studybuddy/database/crud.py

from sqlalchemy.orm import Session
from passlib.context import CryptContext

# Import our own modules for database models and API schemas
from . import models
from studybuddy.api import schemas
from typing import List 

# 1. --- Password Hashing Setup ---
# We create a CryptContext instance, specifying that we want to use the 'bcrypt' algorithm.
# This object will handle both hashing and verifying passwords for us.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """A simple function to hash a given password."""
    return pwd_context.hash(password)

# 2. --- User Creation Function ---
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Creates a new user entry in the database.

    Args:
        db (Session): The database session object for executing queries.
        user (schemas.UserCreate): The user data (email and password) from the API request.

    Returns:
        models.User: The SQLAlchemy User model instance that was just created.
    """
    # Hash the plain-text password from the request before storing it
    hashed_password = get_password_hash(user.password)

    # Create a new instance of our SQLAlchemy `User` model
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password
    )

    # Add the new user instance to the database session
    db.add(db_user)
    
    # Commit the changes to the database (writes the new user to the table)
    db.commit()
    
    # Refresh the `db_user` instance to get the new data from the database, like the auto-generated ID
    db.refresh(db_user)

    return db_user

def get_todos_by_user(db: Session, user_id: int) -> List[models.Todo]:
    """
    Retrieves all to-do items for a specific user.
    """
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).all()


def create_user_todo(db: Session, todo: schemas.TodoCreate, user_id: int) -> models.Todo:
    """
    Creates a new to-do item for a specific user.
    """
    # Create the SQLAlchemy model instance
    db_todo = models.Todo(
        title=todo.title,
        owner_id=user_id
    )
    
    # Add, commit, and refresh
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    
    return db_todo