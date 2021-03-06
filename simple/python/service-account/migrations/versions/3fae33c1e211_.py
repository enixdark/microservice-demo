"""empty message

Revision ID: 3fae33c1e211
Revises: b050dcd37bdb
Create Date: 2018-06-17 15:57:27.881158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fae33c1e211'
down_revision = 'b050dcd37bdb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('delete', sa.Boolean(), nullable=True),
    sa.Column('role', sa.Enum('MEMBER', 'MANAGER', name='userrole'), nullable=True),
    sa.Column('auth_id', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
