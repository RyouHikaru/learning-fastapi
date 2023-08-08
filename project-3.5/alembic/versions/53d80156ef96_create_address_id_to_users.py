"""Create address_id to users

Revision ID: 53d80156ef96
Revises: 64a66840bcd4
Create Date: 2023-08-08 11:23:59.311858

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53d80156ef96'
down_revision: Union[str, None] = '64a66840bcd4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column(
        "address_id", sa.Integer(), nullable=True))
    op.create_foreign_key("address_users_fk", source_table="users", referent_table="address", local_cols=[
                          "address_id"], remote_cols=["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("address_users_fk", table_name="users")
    op.drop_column("users", "address_id")