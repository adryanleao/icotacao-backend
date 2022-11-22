"""quote_proposal_product

Revision ID: a792fe004dcb
Revises: de355d8c98a5
Create Date: 2021-01-06 17:51:53.969856

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a792fe004dcb'
down_revision = 'de355d8c98a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quote_proposal_product',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('manufacturer', sa.String(length=256), nullable=True),
    sa.Column('observation', sa.Text(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('quote_proposal_id', sa.Integer(), nullable=True),
    sa.Column('quote_product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['quote_product_id'], ['quote_product.id'], ),
    sa.ForeignKeyConstraint(['quote_proposal_id'], ['quote_proposal.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.alter_column('quote_product', 'manufacturer',
               existing_type=mysql.VARCHAR(length=256),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('quote_product', 'manufacturer',
               existing_type=mysql.VARCHAR(length=256),
               nullable=False)
    op.drop_table('quote_proposal_product')
    # ### end Alembic commands ###