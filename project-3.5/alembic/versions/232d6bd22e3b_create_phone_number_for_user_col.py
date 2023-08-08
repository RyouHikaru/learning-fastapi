"""create phone number for user col

Revision ID: 232d6bd22e3b
Revises: 
Create Date: 2023-08-08 11:12:39.404952

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '232d6bd22e3b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column(
        "phone_number", sa.String(length=20), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
