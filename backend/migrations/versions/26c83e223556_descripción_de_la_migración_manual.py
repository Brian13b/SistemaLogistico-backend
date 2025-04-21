"""Descripción de la migración manual

Revision ID: 26c83e223556
Revises: ac7e69f2ec87
Create Date: 2025-03-03 11:18:12.264338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26c83e223556'
down_revision: Union[str, None] = 'ac7e69f2ec87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
