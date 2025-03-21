"""Initial migration

Revision ID: 0c40768ce216
Revises: 
Create Date: 2025-03-07 18:25:41.861444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0c40768ce216'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('azure_costs')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('azure_costs',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('usage_date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('service_name', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('cost', sa.NUMERIC(precision=12, scale=4), autoincrement=False, nullable=False),
    sa.Column('currency', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='azure_costs_pkey')
    )
    # ### end Alembic commands ###
