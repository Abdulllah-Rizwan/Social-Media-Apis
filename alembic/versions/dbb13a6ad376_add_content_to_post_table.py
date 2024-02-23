"""add content to post table

Revision ID: dbb13a6ad376
Revises: 765dcd8826b4
Create Date: 2024-02-22 19:57:21.036213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbb13a6ad376'
down_revision: Union[str, None] = '765dcd8826b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Post', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('Post', 'content');
    pass
