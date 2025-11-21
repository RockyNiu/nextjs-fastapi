"""create_role_table_and_update_user

Revision ID: 2a2d371a7751
Revises: 659bcbfc978e
Create Date: 2025-09-11 01:36:27.967875

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2a2d371a7751"
down_revision: Union[str, None] = "659bcbfc978e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create ref_user_role table
    op.create_table(
        "ref_user_role",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("value", sa.String(50), nullable=False),
        sa.UniqueConstraint("value", name="value"),
    )

    # Insert role values
    op.execute("""
        INSERT INTO ref_user_role (id, value) VALUES 
        (1, 'user'),
        (2, 'moderator'),
        (3, 'admin')
    """)

    # Add role_id foreign key column
    op.add_column(
        "users",
        sa.Column(
            "role_id",
            sa.Integer(),
            sa.ForeignKey("ref_user_role.id"),
            nullable=False,
            server_default="1",
        ),
    )


def downgrade() -> None:
    # Remove role_id column and drop ref_user_role table
    op.drop_column("users", "role_id")
    op.drop_table("ref_user_role")
