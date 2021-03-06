"""empty message

Revision ID: e8f2ebd87033
Revises: b595b49924a0
Create Date: 2017-08-27 15:29:36.429973

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e8f2ebd87033'
down_revision = 'b595b49924a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('creation_date', sa.TIMESTAMP(), nullable=True))
    op.drop_column('article', 'create_date')
    op.add_column('user', sa.Column('registration_date', sa.TIMESTAMP(), nullable=True))
    op.drop_column('user', 'register_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('register_date', mysql.TIMESTAMP(), nullable=True))
    op.drop_column('user', 'registration_date')
    op.add_column('article', sa.Column('create_date', mysql.TIMESTAMP(), nullable=True))
    op.drop_column('article', 'creation_date')
    # ### end Alembic commands ###
