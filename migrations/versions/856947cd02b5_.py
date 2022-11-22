"""empty message

Revision ID: 856947cd02b5
Revises: d520a162cce3
Create Date: 2021-01-25 16:39:26.134969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '856947cd02b5'
down_revision = 'd520a162cce3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quote_proposal_product', sa.Column('dont_have', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('quote_proposal_product', 'dont_have')
    # ### end Alembic commands ###