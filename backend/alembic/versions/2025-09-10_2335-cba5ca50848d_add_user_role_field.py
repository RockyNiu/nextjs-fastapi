"""add_user_role_field

Revision ID: cba5ca50848d
Revises: 659bcbfc978e
Create Date: 2025-09-10 23:35:42.138266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cba5ca50848d'
down_revision: Union[str, None] = '659bcbfc978e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add role column to users table
    op.add_column('users', sa.Column('role', sa.Enum('admin', 'moderator', 'user', name='userrole'), nullable=False, server_default='user'))


def downgrade() -> None:
    # Remove role column from users table
    op.drop_column('users', 'role')
    # Drop the enum type
    op.execute("DROP TYPE userrole")
