# In studybuddy/api/schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime

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