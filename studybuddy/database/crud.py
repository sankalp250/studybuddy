# In studybuddy/database/crud.py

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import List

from . import models
from studybuddy.api import schemas

# --- Password Hashing Setup ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# --- User CRUD Functions ---

def get_user(db: Session, user_id: int) -> models.User | None:
    """
    Retrieves a single user by their unique ID.
    (This is the function that was missing)
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> models.User | None:
    """
    Retrieves a single user by their email address.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Creates a new user in the database.
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Todo CRUD Functions ---

def get_todos_by_user(db: Session, user_id: int) -> List[models.Todo]:
    """
    Retrieves all to-do items for a specific user.
    """
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).all()

def create_user_todo(db: Session, todo: schemas.TodoCreate, user_id: int) -> models.Todo:
    """
    Creates a new to-do item and associates it with a user.
    """
    db_todo = models.Todo(title=todo.title, owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo