"""add due_date

Revision ID: fff16bcfff57
Revises: e9f7c865d66c
Create Date: 2026-03-27 21:31:46.960748

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fff16bcfff57'
down_revision: Union[str, Sequence[str], None] = 'e9f7c865d66c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('todos', sa.Column('due_date', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('todos', 'due_date')
