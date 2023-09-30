"""add_sale_related_columns

Revision ID: 4970edbed75a
Revises: 42f4514d2e6e
Create Date: 2023-10-01 00:16:13.071219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '4970edbed75a'
down_revision: Union[str, None] = '42f4514d2e6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add the 'stock' column with a default value of 0
    op.add_column('sales', sa.Column('total', sa.Float(), server_default="0"))
    op.add_column('products', sa.Column('margin', sa.Float(), server_default="0"))


def downgrade():
    # Remove the 'stock' column
    op.drop_column('products', 'stock')
    op.drop_column('sales', 'total')
