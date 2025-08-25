"""add doctor_id to appointments

Revision ID: 77744e0c107f
Revises: 1e64232824be
Create Date: 2025-08-25 14:12:05.494561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77744e0c107f'
down_revision: Union[str, None] = '1e64232824be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
