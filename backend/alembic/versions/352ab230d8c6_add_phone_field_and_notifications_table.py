"""Add phone field and notifications table

Revision ID: 352ab230d8c6
Revises: 
Create Date: 2025-03-25 10:37:29.470893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '352ab230d8c6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activities', sa.Column('status', sa.String(length=50), nullable=True))
    op.alter_column('notifications', 'created_at',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.create_index(op.f('ix_notifications_id'), 'notifications', ['id'], unique=False)
    op.drop_constraint('notifications_ibfk_1', 'notifications', type_='foreignkey')
    op.create_foreign_key(None, 'notifications', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'notifications', type_='foreignkey')
    op.create_foreign_key('notifications_ibfk_1', 'notifications', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_index(op.f('ix_notifications_id'), table_name='notifications')
    op.alter_column('notifications', 'created_at',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.drop_column('activities', 'status')
    # ### end Alembic commands ###
