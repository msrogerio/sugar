"""empty message

Revision ID: 8e3a53f9f5e5
Revises: 2c561a21f408
Create Date: 2022-05-27 18:32:10.531302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e3a53f9f5e5'
down_revision = '2c561a21f408'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('check_progress',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('total_records', sa.Integer(), nullable=True),
    sa.Column('treated_records', sa.Integer(), nullable=True),
    sa.Column('mensage', sa.String(length=1000), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('check_progress')
    # ### end Alembic commands ###
