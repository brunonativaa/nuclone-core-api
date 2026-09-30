"""add_is_noturno_e_limites_conta

Revision ID: 5012781f2dce
Revises: 0fe51eef4e7a
Create Date: 2026-09-23 15:36:14.193432

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5012781f2dce'
down_revision: Union[str, Sequence[str], None] = '0fe51eef4e7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
