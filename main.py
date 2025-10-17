# In main.py

from fastapi import FastAPI
from studybuddy.api import endpoints  # 1. IMPORT the endpoints module

app = FastAPI(
    title="StudyBuddy AI",
    description="An intelligent ecosystem for student productivity.",
    version="0.1.0"
)

# 2. INCLUDE the router from the endpoints module.
#    This makes all endpoints defined in 'endpoints.py' (like /users/)
#    part of our main application.
#    - The `prefix` puts all these routes under '/api'.
#    - The `tags` groups them nicely in the API docs.
app.include_router(endpoints.router, prefix="/api", tags=["Users"])

@app.get("/", tags=["Root"])
def read_root():
    """
    A simple health check endpoint to see if the server is alive.
    """
    return {"message": "Welcome to the StudyBuddy AI API!"}