"""add email, password_hash to provider

Revision ID: 5fed5d47679e
Revises: 352ab230d8c6
Create Date: 2025-03-27 15:25:36.368849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '5fed5d47679e'
down_revision: Union[str, None] = '352ab230d8c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('activities', 'status',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    op.alter_column('providers', 'name',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.alter_column('providers', 'email',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.alter_column('providers', 'password_hash',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('providers', 'password_hash',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('providers', 'email',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.alter_column('providers', 'name',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.alter_column('activities', 'status',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###
