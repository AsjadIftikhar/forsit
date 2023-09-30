"""create_sales_table

Revision ID: ead5f01d67b4
Revises: d6cf1107969f
Create Date: 2023-09-30 17:56:51.803710

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = 'ead5f01d67b4'
down_revision: Union[str, None] = 'd6cf1107969f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'sales',
        Column('id', Integer, primary_key=True, index=True),
        Column('sale_date', DateTime, default=datetime.utcnow),
        Column('quantity', Integer),
        Column('revenue', Float),
        Column('product_id', Integer, ForeignKey("products.id", name="fk_product_id"))
    )
    op.create_index('ix_sales_product_id', 'sales', ['product_id'])


def downgrade() -> None:
    op.drop_index('ix_sales_product_id', 'sales')
    op.drop_table('sales')
