# In studybuddy/api/endpoints.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# NEW: Import the base Exception class to catch errors
from sqlalchemy.exc import SQLAlchemyError 

from studybuddy.database import connection, crud, models
from studybuddy.api import schemas

router = APIRouter()

@router.post("/users/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register_user(
    user: schemas.UserCreate, 
    db: Session = Depends(connection.get_db)
):
    """
    Register a new user in the system.
    """
    # We will wrap the database logic in a try...except block to catch the error
    try:
        # Check if a user with that email already exists
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        
        # If not, create the new user
        return crud.create_user(db=db, user=user)

    # NEW: Catch any SQLAlchemy-related error
    except SQLAlchemyError as e:
        # If an error occurs, we will raise an HTTPException
        # with the specific database error message as the detail.
        # str(e) converts the error object to a readable string.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred with the database: {str(e)}"
        )