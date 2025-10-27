#!/usr/bin/env python
"""
Script to run database migrations
Run this to initialize the database tables
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alembic import command
from alembic.config import Config

def run_migrations():
    """Run Alembic migrations to initialize/update the database."""
    print("Running database migrations...")
    
    try:
        # Configure Alembic
        alembic_cfg = Config("alembic.ini")
        
        # Run migrations to head
        command.upgrade(alembic_cfg, "head")
        print("SUCCESS: Database migrations completed successfully!")
        
    except Exception as e:
        print(f"ERROR: Error running migrations: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_migrations()

