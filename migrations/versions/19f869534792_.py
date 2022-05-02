"""empty message

Revision ID: 19f869534792
Revises: e35e124ff488
Create Date: 2022-05-01 14:00:19.346040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19f869534792'
down_revision = 'e35e124ff488'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_member_member_number'), 'member', ['member_number'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_member_member_number'), table_name='member')
    # ### end Alembic commands ###