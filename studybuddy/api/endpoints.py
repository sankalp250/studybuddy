# In studybuddy/api/endpoints.py (WITH SYSTEM MESSAGE FIX)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Import both HumanMessage and the new SystemMessage
from langchain_core.messages import HumanMessage, SystemMessage
from typing import List

from studybuddy.agents.daily_digest_agent import create_daily_digest_agent
from studybuddy.database import connection, crud, models
from studybuddy.api import schemas

router = APIRouter()
daily_digest_agent = create_daily_digest_agent()

# --- User Endpoints (No change) ---
@router.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=["Users"])
def register_user(user: schemas.UserCreate, db: Session = Depends(connection.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# --- Todo Endpoints (No change) ---
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

# --- AI Agent Endpoint (THIS IS WHERE THE FIX IS) ---
@router.post("/daily-digest/", response_model=schemas.DigestResponse, tags=["AI Agents"])
def get_daily_digest(request: schemas.DigestRequest):
    """
    Takes a user's query, runs the agent with a guiding system prompt, and returns the result.
    """
    try:
        # Define the agent's persona and instructions
        system_prompt = (
            "You are an expert study assistant and career coach. "
            "Your primary goal is to take a user's task or query and use your available tools to provide a comprehensive, helpful, and encouraging response. "
            "You must use the tavily_search_results_json tool to find relevant, up-to-date information before formulating your final answer."
        )
        
        # Format the input with the system message first, then the user's query
        initial_input = {
            "messages": [
                SystemMessage(content=system_prompt),
                HumanMessage(content=request.query)
            ]
        }
        
        final_state = daily_digest_agent.invoke(initial_input)
        final_answer = final_state["messages"][-1].content
        return schemas.DigestResponse(response=final_answer)

    except Exception as e:
        print(f"Agent invocation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request: {e}",
        )