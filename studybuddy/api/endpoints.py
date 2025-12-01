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
from studybuddy.agents.flashcard_agent import create_flashcard_agent
from studybuddy.agents.resume_agent import create_resume_agent
from studybuddy.agents.interview_agent import create_interview_agent
# Optional RAG import - fallback to simple agent if not available
try:
    from studybuddy.agents.interview_agent_rag import prepare_interview_with_rag
except ImportError:
    prepare_interview_with_rag = None
from studybuddy.tools.rag_utils import store_resume
from studybuddy.database import connection, crud, models
from studybuddy.api import schemas
from studybuddy.core import srs_logic

router = APIRouter()

# --- Lazy load agents to avoid startup errors ---
_daily_digest_agent = None
_leetcode_agent = None
_flashcard_agent = None
_resume_agent = None
_interview_agent = None

def get_daily_digest_agent():
    global _daily_digest_agent
    if _daily_digest_agent is None:
        _daily_digest_agent = create_daily_digest_agent(model_name="llama-3.1-8b-instant")
    return _daily_digest_agent

def get_leetcode_agent():
    global _leetcode_agent
    if _leetcode_agent is None:
        _leetcode_agent = create_leetcode_agent(model_name="llama-3.1-8b-instant")
    return _leetcode_agent

def get_flashcard_agent():
    global _flashcard_agent
    if _flashcard_agent is None:
        _flashcard_agent = create_flashcard_agent(model_name="llama-3.1-8b-instant")
    return _flashcard_agent

def get_resume_agent():
    global _resume_agent
    if _resume_agent is None:
        _resume_agent = create_resume_agent(model_name="llama-3.1-8b-instant")
    return _resume_agent

def get_interview_agent():
    global _interview_agent
    if _interview_agent is None:
        _interview_agent = create_interview_agent(model_name="llama-3.1-8b-instant")
    return _interview_agent

# --- User and Todo Endpoints (WORKING) ---
@router.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=["Users"])
def register_user(user: schemas.UserCreate, db: Session = Depends(connection.get_db)):
    try:
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        new_user = crud.create_user(db=db, user=user)
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"User registration error: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

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
def agent_chat(
    request: schemas.ChatRequest,
    db: Session = Depends(connection.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Chat endpoint with RAG-based personalized interview questions.
    Uses LangGraph agent to retrieve relevant resume context and generate personalized questions.
    """
    try:
        # Extract study topic from request or infer from messages
        study_topic = request.study_topic
        if not study_topic:
            # Try to infer from the first user message
            for msg in request.messages:
                if msg.role == "user" and msg.content:
                    # Look for topic hints in the message
                    # This is a fallback - ideally the frontend should send study_topic
                    study_topic = "Interview Preparation"  # Default topic
                    break
            if not study_topic:
                study_topic = "Interview Preparation"
        
        # Check if user has a resume uploaded (for RAG)
        has_resume = current_user.resume_summary is not None
        
        if has_resume and prepare_interview_with_rag is not None:
            # Use RAG-based LangGraph agent for personalized questions
            try:
                response = prepare_interview_with_rag(
                    user_id=current_user.id,
                    study_topic=study_topic,
                    messages=[{"role": m.role, "content": m.content} for m in request.messages],
                    model_name="llama-3.1-8b-instant"
                )
                return schemas.AgentResponse(response=response)
            except Exception as rag_error:
                # Fallback to non-RAG agent if RAG fails
                print(f"RAG agent failed, falling back to simple agent: {rag_error}")
                import traceback
                print(traceback.format_exc())
        
        # Fallback to simple interview agent (no RAG)
        resume_context = ""
        if current_user.resume_summary:
            resume_context = f"\n\nUSER'S RESUME SUMMARY:\n{current_user.resume_summary}\n\nIMPORTANT: When asking questions about projects or experiences, reference specific details from the resume above. Personalize the interview preparation to match the user's actual background."
        
        agent = get_interview_agent()
        response = agent(
            [{"role": m.role, "content": m.content} for m in request.messages],
            resume_context
        )
        return schemas.AgentResponse(response=response)
        
    except Exception as e:
        import traceback
        print(f"Agent chat failed: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

# --- Daily Digest Endpoint ---
@router.post("/daily-digest/", response_model=schemas.AgentResponse, tags=["AI Agents"])
def create_daily_digest(
    request: schemas.DailyDigestRequest,
    db: Session = Depends(connection.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """Generate a daily digest for a given topic using the AI agent."""
    try:
        # Use the daily digest agent to generate content
        # The agent expects a messages list with HumanMessage
        from langchain_core.messages import HumanMessage
        agent = get_daily_digest_agent()
        result = agent.invoke({"messages": [HumanMessage(content=request.query)]})
        
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
        agent = get_leetcode_agent()
        problem_markdown = agent.invoke(problem_input)
        return schemas.AgentResponse(response=problem_markdown)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# --- NEW: Authentication Endpoint ---
@router.post("/token", response_model=schemas.Token, tags=["Authentication"])
def login_for_access_token(
    db: Session = Depends(connection.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    try:
        # Authenticate the user - THIS IS THE CORRECTED PART
        user = crud.get_user_by_email(db, email=form_data.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify password
        if not security.verify_password(form_data.password, user.hashed_password):
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
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any other exceptions and return a 500 error with details
        import traceback
        print(f"Login error: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

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

@router.post("/generate-flashcards/", status_code=status.HTTP_201_CREATED, tags=["Flashcards"])
def generate_and_save_flashcards(
    request: schemas.TextContentRequest,
    db: Session = Depends(connection.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Takes a block of text, generates flashcards from it, and saves them to the user's account.
    Returns the number of flashcards created.
    """
    try:
        # Step 1: Run the flashcard generation agent
        agent = get_flashcard_agent()
        ai_response = agent(request.text_content)
        
        # Step 2: Parse the AI response (should be JSON)
        import json
        import re
        
        # Clean the response to extract JSON
        json_match = re.search(r'\[.*\]', ai_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            json_str = ai_response
        
        try:
            flashcards_data = json.loads(json_str)
            if not isinstance(flashcards_data, list):
                flashcards_data = [flashcards_data]
        except json.JSONDecodeError as e:
            # If JSON parsing fails, create a single flashcard from the entire conversation
            flashcard_schema = schemas.FlashcardCreate(
                question="AI Generated Summary",
                answer=request.text_content[:500]
            )
            crud.create_user_flashcard(db=db, flashcard=flashcard_schema, user_id=current_user.id)
            return {"detail": "Successfully created 1 flashcard from conversation!"}

        # Step 3: Loop through the flashcards and save them to the database
        created_count = 0
        for card_data in flashcards_data:
            if isinstance(card_data, dict) and "question" in card_data and "answer" in card_data:
                flashcard_schema = schemas.FlashcardCreate(
                    question=card_data["question"],
                    answer=card_data["answer"]
                )
                crud.create_user_flashcard(db=db, flashcard=flashcard_schema, user_id=current_user.id)
                created_count += 1
        
        return {"detail": f"Successfully created {created_count} flashcards!"}

    except Exception as e:
        import traceback
        print(f"Flashcard generation endpoint failed: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# --- Resume Endpoints ---
@router.post("/upload-resume/", tags=["Resume"])
def upload_resume(
    request: schemas.TextContentRequest,
    db: Session = Depends(connection.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """Uploads and summarizes a user's resume, then stores it in vector database for RAG."""
    try:
        # Generate summary using AI agent
        agent = get_resume_agent()
        summary = agent(request.text_content)
        
        # Store resume in vector database for RAG retrieval
        try:
            num_chunks = store_resume(
                user_id=current_user.id,
                resume_text=request.text_content,
                resume_summary=summary
            )
            print(f"Stored {num_chunks} resume chunks in vector database for user {current_user.id}")
        except Exception as rag_error:
            # Log error but don't fail the request
            print(f"Warning: Could not store resume in vector DB: {rag_error}")
            print("Resume summary will still be saved, but RAG retrieval may not work.")
        
        # Update user's resume summary in database
        current_user.resume_summary = summary
        db.commit()
        db.refresh(current_user)
        
        return {
            "detail": "Resume uploaded and summarized successfully!",
            "summary": summary,
            "rag_enabled": num_chunks > 0 if 'num_chunks' in locals() else False
        }
    
    except Exception as e:
        import traceback
        print(f"Resume upload failed: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")

@router.get("/resume-summary/", response_model=schemas.ResumeSummary, tags=["Resume"])
def get_resume_summary(
    db: Session = Depends(connection.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """Gets the current user's resume summary."""
    return {"resume_summary": current_user.resume_summary or "No resume uploaded yet."}


