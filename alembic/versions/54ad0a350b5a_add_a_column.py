"""add a column

Revision ID: 54ad0a350b5a
Revises: 04615a16a574
Create Date: 2021-07-06 14:58:39.504784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54ad0a350b5a'
down_revision = '04615a16a574'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))

def downgrade():
    op.drop_column('account', 'last_transaction_date')
