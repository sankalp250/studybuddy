# In studybuddy/api/schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

# --- User Schemas ---

# Properties to receive via API on user creation
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Properties to return via API (never include the password)
class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class DigestRequest(BaseModel):
    query: str

# It will return a JSON object like: {"response": "the agent's answer"}
class DigestResponse(BaseModel):
    response: str

    class Config:
        from_attributes = True # Formerly orm_mode = True

class TodoBase(BaseModel):
    title: str

class TodoCreate(TodoBase):
    pass # No extra fields needed on creation

class Todo(TodoBase):
    id: int
    is_completed: bool
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True # Allows Pydantic to read data from ORM models

# New response model for returning a list of todos
class TodoList(BaseModel):
    todos: List[Todo]

