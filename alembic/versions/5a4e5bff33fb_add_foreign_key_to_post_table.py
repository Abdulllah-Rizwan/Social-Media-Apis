"""add foreign key to post table

Revision ID: 5a4e5bff33fb
Revises: 5bc49db16009
Create Date: 2024-02-23 09:38:34.398824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a4e5bff33fb'
down_revision: Union[str, None] = '5bc49db16009'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Post', sa.Column('owner_id', sa.Integer(), nullable=False));
    op.create_foreign_key('post_user_fk', source_table='Post', referent_table='User', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE');
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name='Post');
    op.drop_column('Post', 'owner_id');
    pass
