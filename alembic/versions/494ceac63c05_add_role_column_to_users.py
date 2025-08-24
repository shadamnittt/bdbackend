"""Add role column to users

Revision ID: 494ceac63c05
Revises: 2e0d1ecccabc
Create Date: 2025-08-19 03:39:44.222221
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '494ceac63c05'
down_revision: Union[str, None] = '2e0d1ecccabc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Добавляем колонку role с разрешением NULL
    op.add_column('users', sa.Column('role', sa.String(), nullable=True))

    # 2. Заполняем существующие строки значением 'user'
    op.execute("UPDATE users SET role = 'user' WHERE role IS NULL")

    # 3. Делаем колонку обязательной (NOT NULL)
    op.alter_column('users', 'role', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'role')
