# In studybuddy/api/endpoints.py (FINAL ROBUST VERSION)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing import List

from studybuddy.agents.daily_digest_agent import create_daily_digest_agent
from studybuddy.database import connection, crud, models
from studybuddy.api import schemas

router = APIRouter()
# We are upgrading the agent's brain by changing the model inside this function
daily_digest_agent = create_daily_digest_agent(model_name="llama3-70b-8192")

# --- User and Todo Endpoints (No Changes Needed) ---
@router.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=["Users"])
def register_user(user: schemas.UserCreate, db: Session = Depends(connection.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
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

# --- UPGRADED AI Agent Endpoint ---
@router.post("/agent/chat/", response_model=schemas.AgentResponse, tags=["AI Agents"])
def agent_chat(request: schemas.ChatRequest):
    """
    Handles a conversational turn with the more robust AI agent.
    """
    try:
        # 1. Define the agent's core instructions. This is its "persona".
        system_prompt = (
            "You are an expert AI study assistant and technical interviewer. "
            "Your goal is to have a conversation with the user to help them prepare for their task. "
            "Use the 'tavily_search_results_json' tool to find relevant, up-to-date information. "
            "After using your tools, you MUST synthesize the information and provide a clear, final answer to the user. "
            "Never show the user the raw tool calls (like '<function=tavily_search>...')."
        )

        # 2. Convert incoming chat messages to LangChain format
        langchain_messages = []
        for msg in request.messages:
            if msg.role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                langchain_messages.append(AIMessage(content=msg.content))

        # 3. Construct the full input, ALWAYS starting with the system prompt
        full_input_messages = [SystemMessage(content=system_prompt)] + langchain_messages
        
        initial_input = {"messages": full_input_messages}
        
        # 4. Invoke the agent
        final_state = daily_digest_agent.invoke(initial_input)
        final_answer = final_state["messages"][-1].content
        
        return schemas.AgentResponse(response=final_answer)

    except Exception as e:
        print(f"Agent chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))