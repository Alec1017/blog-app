"""empty message

Revision ID: 17d156f5ed4e
Revises: ee0435d1d75d
Create Date: 2017-08-27 14:42:49.789244

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '17d156f5ed4e'
down_revision = 'ee0435d1d75d'
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
    op.add_column('user', sa.Column('register_date', mysql.DATETIME(), nullable=True))
    op.drop_column('user', 'registration_date')
    op.add_column('article', sa.Column('create_date', mysql.DATETIME(), nullable=True))
    op.drop_column('article', 'creation_date')
    # ### end Alembic commands ###
