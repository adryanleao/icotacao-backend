"""empty message

Revision ID: de43f213306b
Revises: 58e344bef73c
Create Date: 2021-01-14 13:41:05.045743

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'de43f213306b'
down_revision = '58e344bef73c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('deleted_at', sa.DateTime(), nullable=True),
                    sa.Column('name', sa.String(length=256), nullable=False),
                    sa.Column('email', sa.String(length=256), nullable=False),
                    sa.Column('cell_phone', sa.String(length=256), nullable=False),
                    sa.Column('cnpj', sa.String(length=256), nullable=True),
                    sa.Column('status', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('company_segment',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('deleted_at', sa.DateTime(), nullable=True),
                    sa.Column('company_id', sa.Integer(), nullable=True),
                    sa.Column('segment_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
                    sa.ForeignKeyConstraint(['segment_id'], ['segment.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('company_address',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('deleted_at', sa.DateTime(), nullable=True),
                    sa.Column('code_post', sa.String(length=256), nullable=True),
                    sa.Column('street', sa.String(length=256), nullable=True),
                    sa.Column('number', sa.String(length=256), nullable=True),
                    sa.Column('district', sa.String(length=256), nullable=True),
                    sa.Column('complement', sa.String(length=256), nullable=True),
                    sa.Column('lat', sa.String(length=256), nullable=True),
                    sa.Column('long', sa.String(length=256), nullable=True),
                    sa.Column('city_id', sa.Integer(), nullable=True),
                    sa.Column('company_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['city_id'], ['city.id'], ),
                    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.drop_index('id', table_name='supplier_segment')
    op.drop_table('supplier_segment')
    op.drop_index('id', table_name='supplier_address')
    op.drop_table('supplier_address')
    op.drop_constraint('quote_proposal_ibfk_4', 'quote_proposal', type_='foreignkey')
    op.drop_column('quote_proposal', 'supplier_id')
    op.drop_constraint('user_ibfk_2', 'user', type_='foreignkey')
    op.drop_column('user', 'birth_date')
    op.drop_column('user', 'genre')
    op.drop_column('user', 'supplier_id')

    op.drop_index('id', table_name='supplier')
    op.drop_table('supplier')

    op.add_column('quote_proposal', sa.Column('company_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'quote_proposal', 'company', ['company_id'], ['id'])
    op.add_column('user', sa.Column('company_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'company', ['company_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('supplier_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('genre', mysql.VARCHAR(length=256), nullable=True))
    op.add_column('user', sa.Column('birth_date', sa.DATE(), nullable=True))
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.create_foreign_key('user_ibfk_2', 'user', 'supplier', ['supplier_id'], ['id'])
    op.drop_column('user', 'company_id')
    op.add_column('quote_proposal',
                  sa.Column('supplier_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'quote_proposal', type_='foreignkey')
    op.create_foreign_key('quote_proposal_ibfk_4', 'quote_proposal', 'supplier', ['supplier_id'], ['id'])
    op.drop_column('quote_proposal', 'company_id')
    op.create_table('supplier_address',
                    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
                    sa.Column('created_at', mysql.DATETIME(), nullable=True),
                    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
                    sa.Column('deleted_at', mysql.DATETIME(), nullable=True),
                    sa.Column('code_post', mysql.VARCHAR(length=256), nullable=True),
                    sa.Column('street', mysql.VARCHAR(length=256), nullable=True),
                    sa.Column('number', mysql.VARCHAR(length=256), nullable=True),
                    sa.Column('district', mysql.VARCHAR(length=256), nullable=True),
                    sa.Column('complement', mysql.VARCHAR(length=256), nullable=True),
                    sa.Column('lat', mysql.VARCHAR(length=256), nullable=True),
                    sa.Column('long', mysql.VARCHAR(length=256), nullable=True),
                    sa.Column('city_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
                    sa.Column('supplier_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['city_id'], ['city.id'], name='supplier_address_ibfk_1'),
                    sa.ForeignKeyConstraint(['supplier_id'], ['supplier.id'], name='supplier_address_ibfk_2'),
                    sa.PrimaryKeyConstraint('id'),
                    mysql_default_charset='latin1',
                    mysql_engine='InnoDB'
                    )
    op.create_index('id', 'supplier_address', ['id'], unique=True)
    op.create_table('supplier',
                    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
                    sa.Column('created_at', mysql.DATETIME(), nullable=True),
                    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
                    sa.Column('deleted_at', mysql.DATETIME(), nullable=True),
                    sa.Column('social_name', mysql.VARCHAR(length=256), nullable=False),
                    sa.Column('email', mysql.VARCHAR(length=256), nullable=False),
                    sa.Column('cell_phone', mysql.VARCHAR(length=256), nullable=False),
                    sa.Column('cnpj', mysql.VARCHAR(length=256), nullable=True),
                    sa.Column('status', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    mysql_default_charset='latin1',
                    mysql_engine='InnoDB'
                    )
    op.create_index('id', 'supplier', ['id'], unique=True)
    op.create_table('supplier_segment',
                    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
                    sa.Column('created_at', mysql.DATETIME(), nullable=True),
                    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
                    sa.Column('deleted_at', mysql.DATETIME(), nullable=True),
                    sa.Column('supplier_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
                    sa.Column('segment_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['segment_id'], ['segment.id'], name='supplier_segment_ibfk_1'),
                    sa.ForeignKeyConstraint(['supplier_id'], ['supplier.id'], name='supplier_segment_ibfk_2'),
                    sa.PrimaryKeyConstraint('id'),
                    mysql_default_charset='latin1',
                    mysql_engine='InnoDB'
                    )
    op.create_index('id', 'supplier_segment', ['id'], unique=True)
    op.drop_table('company_address')
    op.drop_table('company_segment')
    op.drop_table('company')
    # ### end Alembic commands ###
