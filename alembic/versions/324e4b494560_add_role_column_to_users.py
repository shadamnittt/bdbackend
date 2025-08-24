"""Add role column to users

Revision ID: 324e4b494560
Revises: 494ceac63c05
Create Date: 2025-08-19 03:42:01.610826

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '324e4b494560'
down_revision: Union[str, None] = '494ceac63c05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
