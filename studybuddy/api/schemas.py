# In studybuddy/api/schemas.py (CLEANED VERSION)

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

# --- User Schemas ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str
class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config: from_attributes = True

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
    class Config: from_attributes = True

# --- Chat Schemas ---
class ChatMessage(BaseModel):
    role: str
    content: str
class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    study_topic: str | None = None  # Optional study topic for personalized questions

# --- Daily Digest Schema ---
class DailyDigestRequest(BaseModel):
    query: str

# --- LeetCode Schema ---
class LeetCodeRequest(BaseModel):
    topic: str
    difficulty: str

# --- Generic Agent/API Response Schema ---
class AgentResponse(BaseModel):
    response: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None


class FlashcardBase(BaseModel):
    question: str
    answer: str

class FlashcardCreate(FlashcardBase):
    pass # No extra fields needed on creation

class Flashcard(FlashcardBase):
    id: int
    next_review_at: datetime
    owner_id: int
    
    class Config:
        from_attributes = True

class FlashcardReviewRequest(BaseModel):
    # This schema will be used to submit a review for a card
    performance_rating: int


# --- NEW: Flashcard Generation Schema ---
class TextContentRequest(BaseModel):
    text_content: str

class ResumeSummary(BaseModel):
    resume_summary: str

class UserStats(BaseModel):
    total_study_hours: float
    total_flashcards: int
    total_cards_reviewed: int
    active_streak: int
    total_todos: int
    completed_todos: int