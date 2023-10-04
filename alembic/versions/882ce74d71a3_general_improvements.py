"""general improvements

Revision ID: 882ce74d71a3
Revises: 4970edbed75a
Create Date: 2023-10-04 11:34:30.564518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '882ce74d71a3'
down_revision: Union[str, None] = '4970edbed75a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_check_constraint(
        "check_price_positive",
        "products",
        sa.text("price > 0.0")
    )

    op.create_index(
        "idx_category_id",
        "products",
        ["category_id"]
    )


def downgrade():
    op.drop_constraint("check_price_positive", "products", type_="check")

    op.drop_index("idx_category_id", "products")
