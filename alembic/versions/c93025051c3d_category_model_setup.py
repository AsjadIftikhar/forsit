"""Category Model Setup

Revision ID: c93025051c3d
Revises: 
Create Date: 2023-09-30 17:47:28.043852

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, Integer, String

# revision identifiers, used by Alembic.
revision: str = 'c93025051c3d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'categories',
        Column('id', Integer, primary_key=True, index=True),
        Column('name', String, unique=True, index=True)
    )


def downgrade() -> None:
    op.drop_table('categories')
