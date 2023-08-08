"""Create address table

Revision ID: 64a66840bcd4
Revises: 232d6bd22e3b
Create Date: 2023-08-08 11:19:06.211931

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64a66840bcd4'
down_revision: Union[str, None] = '232d6bd22e3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("address",
                    sa.Column("id", sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column("address1", sa.String(
                        length=100), nullable=False),
                    sa.Column("address2", sa.String(
                        length=100), nullable=False),
                    sa.Column("city", sa.String(length=50), nullable=False),
                    sa.Column("state", sa.String(length=50), nullable=False),
                    sa.Column("country", sa.String(length=30), nullable=False),
                    sa.Column("postalcode", sa.String(
                        length=10), nullable=False),
                    )


def downgrade() -> None:
    op.drop_table("address")
