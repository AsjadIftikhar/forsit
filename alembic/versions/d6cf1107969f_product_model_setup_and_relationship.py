"""Product Model Setup and Relationship

Revision ID: d6cf1107969f
Revises: c93025051c3d
Create Date: 2023-09-30 17:50:25.967046

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, Integer, String, Float, ForeignKey

# revision identifiers, used by Alembic.
revision: str = 'd6cf1107969f'
down_revision: Union[str, None] = 'c93025051c3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'products',
        Column('id', Integer, primary_key=True, index=True),
        Column('name', String, index=True),
        Column('description', String),
        Column('price', Float),
        Column('category_id', Integer, ForeignKey("categories.id", name="fk_category_id"))
    )
    op.create_index('ix_products_category_id', 'products', ['category_id'])


def downgrade():
    op.drop_index('ix_products_category_id', 'products')
    op.drop_table('products')
