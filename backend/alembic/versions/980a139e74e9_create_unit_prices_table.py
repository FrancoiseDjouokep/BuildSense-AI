"""create_unit_prices_table

Revision ID: 980a139e74e9
Revises: c42d6f4c1aa1
Create Date: 2026-08-12 11:29:16.038986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '980a139e74e9'
down_revision: Union[str, Sequence[str], None] = 'c42d6f4c1aa1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
