"""Creacion de los modelos

Revision ID: ac7e69f2ec87
Revises: a4b3d31a9aad
Create Date: 2025-03-03 10:46:02.025256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac7e69f2ec87'
down_revision: Union[str, None] = 'a4b3d31a9aad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
