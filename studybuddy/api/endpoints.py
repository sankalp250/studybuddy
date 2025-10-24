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

@router.post("/users/{user_id}/todos/", response_model=schemas.Todo, tags=["Todos"])
def create_todo_for_user(user_id: int, todo: schemas.TodoCreate, db: Session = Depends(connection.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_todo(db=db, todo=todo, user_id=user_id)

@router.get("/users/{user_id}/todos/", response_model=List[schemas.Todo], tags=["Todos"])
def read_user_todos(user_id: int, db: Session = Depends(connection.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_todos_by_user(db=db, user_id=user_id)

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
    """
    Logs in a user and returns a JWT access token.
    FastAPI expects the client to send 'username' and 'password' in a form.
    """
    # 1. Authenticate the user
    user = crud.get_user_by_email(db, email=form_data.username) # The form uses 'username' field for email
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 2. Create the token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # 3. Return the token
    return {"access_token": access_token, "token_type": "bearer"}