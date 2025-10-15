# In main.py

from fastapi import FastAPI

# Create the main FastAPI application instance
# We can add metadata like title, version, etc.
app = FastAPI(
    title="StudyBuddy AI",
    description="An intelligent ecosystem for student productivity.",
    version="0.1.0"
)

# Define our first API endpoint
@app.get("/", tags=["Root"])
def read_root():
    """
    A simple health check endpoint.
    Returns a welcome message when the server is running.
    """
    return {"message": "Welcome to the StudyBuddy AI API!"}

# You can add more endpoints here in the future
# For example, an endpoint to get all users