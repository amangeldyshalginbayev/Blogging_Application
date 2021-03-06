"""added mobile_phone field to User model

Revision ID: a4eb6356541a
Revises: f4e0480e608c
Create Date: 2020-06-08 16:32:19.518538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4eb6356541a'
down_revision = 'f4e0480e608c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('mobile_phone', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'mobile_phone')
    # ### end Alembic commands ###
