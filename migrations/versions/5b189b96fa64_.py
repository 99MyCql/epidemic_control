"""empty message

Revision ID: 5b189b96fa64
Revises: dcd25fceb321
Create Date: 2022-05-07 21:23:47.163715

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5b189b96fa64'
down_revision = 'dcd25fceb321'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('member', 'role',
               existing_type=mysql.VARCHAR(length=20),
               comment='角色。1代表普通成员，2代表管理员。',
               existing_comment='角色。1代表普通成员，2代表管理员',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('member', 'role',
               existing_type=mysql.VARCHAR(length=20),
               comment='角色。1代表普通成员，2代表管理员',
               existing_comment='角色。1代表普通成员，2代表管理员。',
               existing_nullable=True)
    # ### end Alembic commands ###
