"""mandate phone number

Revision ID: a1beb5e3bc63
Revises: 9c119b267449
Create Date: 2026-11-11 16:18:11.787341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1beb5e3bc63'
down_revision: Union[str, Sequence[str], None] = '9c119b267449'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("users", "phone_number", nullable= False)
    


def downgrade() -> None:
    """Downgrade schema."""
    pass
