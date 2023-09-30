"""add_stock_column

Revision ID: 42f4514d2e6e
Revises: 6fc80c342f78
Create Date: 2023-09-30 23:07:42.063098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '42f4514d2e6e'
down_revision: Union[str, None] = '6fc80c342f78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add the 'stock' column with a default value of 0
    op.add_column('products', sa.Column('stock', sa.Integer(), server_default="0"))

    # Update existing rows to set 'stock' to 0
    op.execute("UPDATE products SET stock = 0 WHERE stock IS NULL")


def downgrade():
    # Remove the 'stock' column
    op.drop_column('products', 'stock')
