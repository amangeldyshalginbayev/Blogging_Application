"""added is_activated column to user table

Revision ID: f4e0480e608c
Revises: ddbfd1e3cf08
Create Date: 2020-06-05 18:58:58.728429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4e0480e608c'
down_revision = 'ddbfd1e3cf08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_activated', sa.Boolean(), server_default='false', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_activated')
    # ### end Alembic commands ###
