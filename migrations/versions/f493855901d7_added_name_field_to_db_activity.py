"""added name field to db_activity

Revision ID: f493855901d7
Revises: 7bd207bdf95a
Create Date: 2021-08-26 12:42:41.044996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f493855901d7'
down_revision = '7bd207bdf95a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('db_activity', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('db_activity', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###
