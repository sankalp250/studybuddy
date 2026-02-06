# In studybuddy/database/crud.py

from sqlalchemy.orm import Session
from typing import List
from studybuddy.core import security # We import our new security module
from sqlalchemy.sql import func
from . import models
from studybuddy.api import schemas
from datetime import datetime, timezone
from . import models # This duplicate import is here in original, keeping or ignoring. I'll just leave it be in the top part, but I can't edit top part easily without seeing it all again or being careful. 
# actually I'll just add the function at the end and the import at the top using separate ReplaceChunk if I can, but replace_file_content only does one chunk unless I use multi_replace.
# I'll use multi_replace_file_content to add import at top and function at bottom.

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

def create_user_flashcard(db: Session, flashcard: schemas.FlashcardCreate, user_id: int) -> models.Flashcard:
    """Creates a new flashcard for a specific user."""
    db_flashcard = models.Flashcard(
        question=flashcard.question,
        answer=flashcard.answer,
        owner_id=user_id
    )
    db.add(db_flashcard)
    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard

def get_due_flashcards_for_user(db: Session, user_id: int) -> List[models.Flashcard]:
    """Retrieves all flashcards for a user that are due for review today."""
    now = datetime.now(timezone.utc)
    return db.query(models.Flashcard).filter(
        models.Flashcard.owner_id == user_id,
        models.Flashcard.next_review_at <= now
    ).all()

def get_flashcard(db: Session, flashcard_id: int, user_id: int) -> models.Flashcard | None:
    """Retrieves a single flashcard by its ID, ensuring it belongs to the correct user."""
    return db.query(models.Flashcard).filter(
        models.Flashcard.id == flashcard_id,
        models.Flashcard.owner_id == user_id
    ).first()

def get_user_statistics(db: Session, user_id: int) -> dict:
    """Calculates user statistics for analytics."""
    total_todos = db.query(models.Todo).filter(models.Todo.owner_id == user_id).count()
    completed_todos = db.query(models.Todo).filter(models.Todo.owner_id == user_id, models.Todo.is_completed == True).count()
    total_flashcards = db.query(models.Flashcard).filter(models.Flashcard.owner_id == user_id).count()
    
    # Sum of all reviews
    total_reviews = db.query(func.sum(models.Flashcard.reviews)).filter(models.Flashcard.owner_id == user_id).scalar() or 0
    
    return {
        "total_study_hours": round(total_reviews * 0.05, 2), # Estimate: 3 min (0.05h) per review
        "total_flashcards": total_flashcards,
        "total_cards_reviewed": total_reviews,
        "active_streak": 0, # Not tracked yet
        "total_todos": total_todos,
        "completed_todos": completed_todos
    }