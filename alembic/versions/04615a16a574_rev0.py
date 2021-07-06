"""rev0

Revision ID: 04615a16a574
Revises: 
Create Date: 2021-07-06 14:57:04.935206

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04615a16a574'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )

def downgrade():
    op.drop_table('account')
