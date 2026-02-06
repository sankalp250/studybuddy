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
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
