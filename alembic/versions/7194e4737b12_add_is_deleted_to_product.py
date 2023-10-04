"""add is_deleted to product

Revision ID: 7194e4737b12
Revises: 882ce74d71a3
Create Date: 2023-10-04 11:38:18.833294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '7194e4737b12'
down_revision: Union[str, None] = '882ce74d71a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('products', sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('FALSE'), nullable=False))


def downgrade():
    op.drop_column('products', 'is_deleted')
