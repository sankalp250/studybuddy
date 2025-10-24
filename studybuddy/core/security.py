# In studybuddy/core/security.py

from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt

from studybuddy.core.config import settings

# --- Password Hashing (Moved from crud.py) ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if a plain password matches a hashed one."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)

# --- JWT Token Creation (NEW) ---
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Creates a new JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default expiration time of 15 minutes if not provided
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt