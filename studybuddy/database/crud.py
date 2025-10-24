# In studybuddy/database/crud.py

from sqlalchemy.orm import Session
from typing import List
from studybuddy.core import security # We import our new security module
from . import models
from studybuddy.api import schemas

# --- User CRUD Functions ---

def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = security.get_password_hash(user.password) # Use security module
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Todo CRUD Functions ---
def get_todos_by_user(db: Session, user_id: int) -> List[models.Todo]:
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).all()

def create_user_todo(db: Session, todo: schemas.TodoCreate, user_id: int) -> models.Todo:
    db_todo = models.Todo(title=todo.title, owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo