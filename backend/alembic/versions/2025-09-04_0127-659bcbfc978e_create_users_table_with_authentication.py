"""Create users table with authentication

Revision ID: 659bcbfc978e
Revises: 
Create Date: 2025-09-04 01:27:06.903765

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utc


# revision identifiers, used by Alembic.
revision: str = '659bcbfc978e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('email_verified', sa.Boolean(), nullable=False),
    sa.Column('email_verification_token', sa.String(length=255), nullable=True),
    sa.Column('password_reset_token', sa.String(length=255), nullable=True),
    sa.Column('password_reset_expires', sa.DateTime(), nullable=True),
    sa.Column('date_created', sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('date_updated', sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)


def downgrade() -> None:
    op.drop_table('users')
