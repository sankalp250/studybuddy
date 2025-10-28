"""
Quick script to create all database tables directly
Run this on your Render backend to create the tables
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import database models and connection
from studybuddy.database.models import Base
from studybuddy.database.connection import engine

def create_tables():
    """Create all tables directly using SQLAlchemy Base metadata"""
    print("Creating database tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("SUCCESS: All tables created successfully!")
        
        # Verify tables were created
        with engine.connect() as conn:
            result = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            tables = [row[0] for row in result]
            print(f"Created tables: {', '.join(tables)}")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    create_tables()

