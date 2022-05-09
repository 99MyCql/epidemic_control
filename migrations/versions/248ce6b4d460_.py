"""empty message

Revision ID: 248ce6b4d460
Revises: 54ff6ee01b08
Create Date: 2022-05-09 10:48:32.530718

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '248ce6b4d460'
down_revision = '54ff6ee01b08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('member', sa.Column('role', sa.Enum('common', 'admin', name='role'), nullable=True, comment='角色，枚举类型。'))
    op.drop_column('member', 'role1')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('member', sa.Column('role1', mysql.ENUM('common', 'admin'), nullable=True, comment='角色。1代表普通成员，2代表管理员。'))
    op.drop_column('member', 'role')
    # ### end Alembic commands ###