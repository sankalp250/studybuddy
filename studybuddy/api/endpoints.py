# In studybuddy/api/endpoints.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# New imports for our agent
from langchain_core.messages import HumanMessage
from studybuddy.agents.daily_digest_agent import create_daily_digest_agent

from studybuddy.database import connection, crud, models
from studybuddy.api import schemas

# Create a new router for API logic
router = APIRouter()

# --- Pre-load the Agent ---
# We create the agent once when the application starts.
# This avoids the slow process of re-creating it for every single request.
daily_digest_agent = create_daily_digest_agent()

# --- User Registration Endpoint (No changes) ---
@router.post("/users/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED, tags=["Users"])
def register_user(
    user: schemas.UserCreate, 
    db: Session = Depends(connection.get_db)
):
    """Register a new user."""
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return crud.create_user(db=db, user=user)

# --- NEW: Daily Digest Agent Endpoint ---
@router.post("/daily-digest/", response_model=schemas.DigestResponse, tags=["AI Agents"])
def get_daily_digest(request: schemas.DigestRequest):
    """
    Takes a user's query, runs the daily digest agent, and returns the result.
    """
    try:
        # 1. Format the input for the agent
        initial_input = {"messages": [HumanMessage(content=request.query)]}
        
        # 2. Invoke the agent. This runs the full loop and gets the final state.
        final_state = daily_digest_agent.invoke(initial_input)
        
        # 3. Extract the final answer from the last message in the state
        final_answer = final_state["messages"][-1].content
        
        # 4. Return the response
        return schemas.DigestResponse(response=final_answer)

    except Exception as e:
        # If the agent fails for any reason, return an internal server error.
        print(f"Agent invocation failed: {e}") # For logging/debugging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request: {e}",
        )