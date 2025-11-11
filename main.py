# In main.py

from fastapi import FastAPI
from studybuddy.api import endpoints  # 1. IMPORT the endpoints module

# Import for database initialization
from alembic import command
from alembic.config import Config
import os
from studybuddy.database.connection import Base, engine

app = FastAPI(
    title="StudyBuddy AI",
    description="An intelligent ecosystem for student productivity.",
    version="0.1.0"
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """
    Initialize database tables using Alembic migrations on startup.
    This ensures tables exist before handling any requests.
    """
    import asyncio
    # Run migrations in background to avoid blocking server startup
    asyncio.create_task(run_migrations_async())

async def run_migrations_async():
    """Run database migrations asynchronously."""
    try:
        # Configure Alembic
        alembic_cfg = Config("alembic.ini")
        
        # Run migrations to ensure database is up to date
        command.upgrade(alembic_cfg, "head")
        print("✓ Database migrations completed successfully")
    except Exception as e:
        print(f"⚠ Warning: Could not run database migrations: {e}")
        print("⚠ This might be okay if the database is already initialized.")
    finally:
        # As an extra safety net, ensure required tables exist even if Alembic didn't run.
        # This is idempotent and safe on PostgreSQL/SQLite; it only creates missing tables.
        try:
            Base.metadata.create_all(bind=engine)
            print("✓ Verified DB schema: ensured core tables exist")
        except Exception as e:
            print(f"⚠ Warning: Could not ensure tables via SQLAlchemy metadata: {e}")

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