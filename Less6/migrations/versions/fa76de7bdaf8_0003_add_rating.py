"""0003_add rating

Revision ID: fa76de7bdaf8
Revises: 514d55fb4f0e
Create Date: 2024-03-14 17:53:27.463294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa76de7bdaf8'
down_revision = '514d55fb4f0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quotes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.Integer(), server_default='1', nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quotes', schema=None) as batch_op:
        batch_op.drop_column('rating')

    # ### end Alembic commands ###