# In studybuddy/api/endpoints.py (CLEANED VERSION)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from studybuddy.core import security
from studybuddy.core.config import settings
from datetime import timedelta
from studybuddy.agents.daily_digest_agent import create_daily_digest_agent
from studybuddy.agents.leetcode_agent import create_leetcode_agent
from studybuddy.database import connection, crud, models
from studybuddy.api import schemas
from studybuddy.core import srs_logic

router = APIRouter()

# --- Load the working agents at startup ---
daily_digest_agent = create_daily_digest_agent(model_name="llama-3.1-8b-instant")
leetcode_agent = create_leetcode_agent(model_name="llama-3.1-8b-instant")

# --- User and Todo Endpoints (WORKING) ---
@router.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=["Users"])
def register_user(user: schemas.UserCreate, db: Session = Depends(connection.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.post("/todos/", response_model=schemas.Todo, tags=["Todos"])
def create_todo_for_user(
    todo: schemas.TodoCreate,
    db: Session = Depends(connection.get_db),
    # This dependency will automatically run get_current_user,
    # ensuring only logged-in users can access this.
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Creates a new to-do item for the currently authenticated user.
    """
    return crud.create_user_todo(db=db, todo=todo, user_id=current_user.id)

@router.get("/todos/", response_model=List[schemas.Todo], tags=["Todos"])
def read_user_todos(
    db: Session = Depends(connection.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Retrieves all to-do items for the currently authenticated user.
    """
    return crud.get_todos_by_user(db=db, user_id=current_user.id)

# --- AI Chat Agent Endpoint (WORKING) ---
@router.post("/agent/chat/", response_model=schemas.AgentResponse, tags=["AI Agents"])
def agent_chat(request: schemas.ChatRequest):
    try:
        system_prompt = "You are an expert AI study assistant..."
        langchain_messages = [SystemMessage(content=system_prompt)]
        for msg in request.messages:
            if msg.role == "user": langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant": langchain_messages.append(AIMessage(content=msg.content))
        final_state = daily_digest_agent.invoke({"messages": langchain_messages})
        return schemas.AgentResponse(response=final_state["messages"][-1].content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Daily Digest Endpoint ---
@router.post("/daily-digest/", response_model=schemas.AgentResponse, tags=["AI Agents"])
def create_daily_digest(request: schemas.DailyDigestRequest):
    """Generate a daily digest for a given topic using the AI agent."""
    try:
        # Use the daily digest agent to generate content
        # The agent expects a messages list with HumanMessage
        from langchain_core.messages import HumanMessage
        result = daily_digest_agent.invoke({"messages": [HumanMessage(content=request.query)]})
        
        # Extract the final response from the agent
        final_message = result["messages"][-1]
        if hasattr(final_message, 'content'):
            return schemas.AgentResponse(response=final_message.content)
        else:
            return schemas.AgentResponse(response=str(final_message))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate daily digest: {str(e)}")

@router.post("/generate-leetcode/", response_model=schemas.AgentResponse, tags=["AI Agents"])
def generate_leetcode_problem(request: schemas.LeetCodeRequest):
    """Takes a topic and difficulty, runs the LeetCode agent, and returns a Markdown problem."""
    try:
        problem_input = {"topic": request.topic, "difficulty": request.difficulty}
        problem_markdown = leetcode_agent.invoke(problem_input)
        return schemas.AgentResponse(response=problem_markdown)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# --- NEW: Authentication Endpoint ---
@router.post("/token", response_model=schemas.Token, tags=["Authentication"])
def login_for_access_token(
    db: Session = Depends(connection.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    # Authenticate the user - THIS IS THE CORRECTED PART
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create the access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/flashcards/", response_model=schemas.Flashcard, tags=["Flashcards"])
def create_flashcard_for_user(
    flashcard: schemas.FlashcardCreate,
    db: Session = Depends(connection.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """Creates a new flashcard for the currently authenticated user."""
    return crud.create_user_flashcard(db=db, flashcard=flashcard, user_id=current_user.id)

@router.get("/flashcards/due/", response_model=List[schemas.Flashcard], tags=["Flashcards"])
def read_due_flashcards(
    db: Session = Depends(connection.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """Retrieves all flashcards that are due for review for the current user."""
    return crud.get_due_flashcards_for_user(db=db, user_id=current_user.id)

@router.post("/flashcards/{flashcard_id}/review/", response_model=schemas.Flashcard, tags=["Flashcards"])
def review_flashcard(
    flashcard_id: int,
    review: schemas.FlashcardReviewRequest,
    db: Session = Depends(connection.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """Updates a flashcard's SRS data after a user reviews it."""
    db_flashcard = crud.get_flashcard(db, flashcard_id=flashcard_id, user_id=current_user.id)
    if not db_flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    
    # Use our SRS algorithm to calculate the new review data
    updated_flashcard = srs_logic.calculate_srs_update(db_flashcard, review.performance_rating)
    
    # Save the changes to the database
    db.commit()
    db.refresh(updated_flashcard)
    
    return updated_flashcard


