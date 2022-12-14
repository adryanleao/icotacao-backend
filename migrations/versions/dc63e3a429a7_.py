"""empty message

Revision ID: dc63e3a429a7
Revises: c6755b4a5cb6
Create Date: 2021-01-14 21:08:00.295104

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'dc63e3a429a7'
down_revision = 'c6755b4a5cb6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quote', sa.Column('observation', sa.Text(), nullable=True))
    op.drop_column('quote', 'date_observation')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quote', sa.Column('date_observation', mysql.TEXT(), nullable=True))
    op.drop_column('quote', 'observation')
    # ### end Alembic commands ###
