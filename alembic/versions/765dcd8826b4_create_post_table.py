""" create post table

Revision ID: 765dcd8826b4
Revises: 
Create Date: 2024-02-22 19:44:50.247749

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '765dcd8826b4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('Post', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),sa.Column('title', sa.Text(), nullable=False));
    pass


def downgrade() -> None:
    op.drop_table("Post")
    pass
