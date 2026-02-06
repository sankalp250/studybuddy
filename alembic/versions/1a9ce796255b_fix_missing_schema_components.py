"""Fix missing schema components

Revision ID: 1a9ce796255b
Revises: 9b02a4774cbd
Create Date: 2026-02-07 01:08:42.290530

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '1a9ce796255b'
down_revision: Union[str, Sequence[str], None] = '9b02a4774cbd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Safe manual fix
    # Add resume_summary if not exists
    op.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS resume_summary TEXT")
    
    # Add flashcards table
    op.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            next_review_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
            interval INTEGER DEFAULT 1 NOT NULL,
            ease_factor FLOAT DEFAULT 2.5 NOT NULL,
            reviews INTEGER DEFAULT 0 NOT NULL,
            owner_id INTEGER NOT NULL REFERENCES users(id),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
    """)
    
    # Add is_completed to todos
    op.execute("ALTER TABLE todos ADD COLUMN IF NOT EXISTS is_completed BOOLEAN DEFAULT FALSE")


def downgrade() -> None:
    pass
