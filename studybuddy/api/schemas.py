# In studybuddy/api/schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

# --- User Schemas ---

class UserCreate(BaseModel):
    email: EmailStr
    password: str

# <<< CHANGE THIS CLASS NAME
class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

# --- Digest Schemas ---
class DigestRequest(BaseModel):
    query: str

class DigestResponse(BaseModel):
    response: str

# --- Todo Schemas ---
class TodoBase(BaseModel):
    title: str

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    is_completed: bool
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TodoList(BaseModel):
    todos: List[Todo]