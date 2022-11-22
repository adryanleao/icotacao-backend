"""code_alpha3 nullable

Revision ID: 76f4d702c4ab
Revises: a41e5299e35b
Create Date: 2020-12-22 14:34:38.219557

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '76f4d702c4ab'
down_revision = 'a41e5299e35b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('country', 'code_alpha3',
               existing_type=mysql.VARCHAR(length=3),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('country', 'code_alpha3',
               existing_type=mysql.VARCHAR(length=3),
               nullable=False)
    # ### end Alembic commands ###