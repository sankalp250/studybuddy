# In studybuddy/api/endpoints.py (CHAT-ENABLED)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Import AIMessage for constructing the chat history
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing import List

from studybuddy.agents.daily_digest_agent import create_daily_digest_agent
from studybuddy.database import connection, crud, models
from studybuddy.api import schemas

router = APIRouter()
daily_digest_agent = create_daily_digest_agent()

# ... (User and Todo endpoints remain unchanged)
@router.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=["Users"])
def register_user(user: schemas.UserCreate, db: Session = Depends(connection.get_db)):
    # ...
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.post("/users/{user_id}/todos/", response_model=schemas.Todo, tags=["Todos"])
def create_todo_for_user(user_id: int, todo: schemas.TodoCreate, db: Session = Depends(connection.get_db)):
    # ...
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_todo(db=db, user_id=user_id)

@router.get("/users/{user_id}/todos/", response_model=List[schemas.Todo], tags=["Todos"])
def read_user_todos(user_id: int, db: Session = Depends(connection.get_db)):
    # ...
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_todos_by_user(db=db, user_id=user_id)

# --- UPGRADED AI Agent Endpoint ---
# It now uses the new ChatRequest and AgentResponse schemas
@router.post("/agent/chat/", response_model=schemas.AgentResponse, tags=["AI Agents"])
def agent_chat(request: schemas.ChatRequest):
    """
    Handles a conversational turn with the AI agent.
    Takes the entire chat history and returns the agent's next response.
    """
    try:
        # Convert our simple ChatMessage schema to LangChain's message objects
        langchain_messages = []
        for msg in request.messages:
            if msg.role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                langchain_messages.append(AIMessage(content=msg.content))
        
        initial_input = {"messages": langchain_messages}
        
        final_state = daily_digest_agent.invoke(initial_input)
        final_answer = final_state["messages"][-1].content
        return schemas.AgentResponse(response=final_answer)

    except Exception as e:
        print(f"Agent chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))