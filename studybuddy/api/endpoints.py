# In studybuddy/api/endpoints.py (CLEANED VERSION)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing import List

from studybuddy.agents.daily_digest_agent import create_daily_digest_agent
from studybuddy.database import connection, crud, models
from studybuddy.api import schemas

router = APIRouter()

# --- Load the working agent at startup ---
daily_digest_agent = create_daily_digest_agent(model_name="llama3-70b-8192")

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