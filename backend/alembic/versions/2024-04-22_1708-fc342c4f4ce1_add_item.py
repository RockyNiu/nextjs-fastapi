"""Add Item

Revision ID: fc342c4f4ce1
Revises: 
Create Date: 2024-04-22 17:08:19.612062

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fc342c4f4ce1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    items = op.create_table(
        "items",
        sa.Column(
            "id", mysql.INTEGER(unsigned=True), autoincrement=True, nullable=False
        ),
        sa.Column("name", sa.VARCHAR(length=255), nullable=False),
        sa.Column(
            "date_created",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "date_updated",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_items_id"), "items", ["id"], unique=False)
    op.bulk_insert(
        items,
        [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"},
        ],
    )


def downgrade() -> None:
    op.drop_table("items")
