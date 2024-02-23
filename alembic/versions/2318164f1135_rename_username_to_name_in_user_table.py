"""rename username to name in user table

Revision ID: 2318164f1135
Revises: b7a369c39195
Create Date: 2024-02-23 17:44:52.942919

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2318164f1135'
down_revision: Union[str, None] = 'b7a369c39195'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('User', 'username', new_column_name='name')
    pass


def downgrade() -> None:
    op.drop_column('User', 'name')
    pass
