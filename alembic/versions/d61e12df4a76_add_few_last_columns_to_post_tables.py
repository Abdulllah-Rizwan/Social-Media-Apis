"""Add few last columns to post tables

Revision ID: d61e12df4a76
Revises: 5a4e5bff33fb
Create Date: 2024-02-23 09:53:08.615585

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd61e12df4a76'
down_revision: Union[str, None] = '5a4e5bff33fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Post',sa.Column('published',sa.Boolean(),nullable=False,server_default="TRUE"))
    op.add_column('Post', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')));
    op.add_column('Post',sa.Column('updated_at',sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('Post', 'published')
    op.drop_column('Post', 'created_at')
    op.drop_column('Post', 'updated_at')
    pass
