"""empty message

Revision ID: 136db5146cc5
Revises: 1299b88f2c20
Create Date: 2018-02-04 11:50:36.839371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '136db5146cc5'
down_revision = '1299b88f2c20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('result', sa.Column('id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('result', 'id')
    # ### end Alembic commands ###
