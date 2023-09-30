"""create inventory tracking table

Revision ID: 6fc80c342f78
Revises: ead5f01d67b4
Create Date: 2023-09-30 22:57:22.858456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '6fc80c342f78'
down_revision: Union[str, None] = 'ead5f01d67b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "inventory_tracking",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("product_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ),
        sa.PrimaryKeyConstraint("id"),
        sa.Index("idx_inventory_tracking_product_id", "product_id"),
        sa.Index("idx_inventory_tracking_timestamp", "timestamp"),
    )


def downgrade() -> None:
    op.drop_index("idx_inventory_tracking_product_id", table_name="inventory_tracking")
    op.drop_index("idx_inventory_tracking_timestamp", table_name="inventory_tracking")
    op.drop_table("inventory_tracking")
