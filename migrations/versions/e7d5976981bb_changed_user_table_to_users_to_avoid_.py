"""changed User table to Users to avoid clash with Posgres User table.

Revision ID: e7d5976981bb
Revises: f78b2382cb82
Create Date: 2021-08-15 13:14:00.120809

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e7d5976981bb'
down_revision = 'f78b2382cb82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('image_file', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('strava_id', sa.Integer(), nullable=True),
    sa.Column('strava_scope', sa.Text(), nullable=True),
    sa.Column('strava_access_token', sa.String(length=40), nullable=True),
    sa.Column('strava_token_expires_at', sa.DateTime(), nullable=True),
    sa.Column('strava_refresh_token', sa.String(length=40), nullable=True),
    sa.Column('strava_athlete_info', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('strava_id'),
    sa.UniqueConstraint('username')
    )

    with op.batch_alter_table('db_activity', schema=None) as batch_op:
        batch_op.drop_constraint('db_activity_user_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('db_activity_athlete_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['athlete_id'], ['strava_id'])
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])

    op.drop_table('user')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('db_activity', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('db_activity_athlete_id_fkey', 'user', ['athlete_id'], ['strava_id'])
        batch_op.create_foreign_key('db_activity_user_id_fkey', 'user', ['user_id'], ['id'])

    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('image_file', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=60), autoincrement=False, nullable=False),
    sa.Column('strava_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('strava_scope', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('strava_access_token', sa.VARCHAR(length=40), autoincrement=False, nullable=True),
    sa.Column('strava_token_expires_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('strava_refresh_token', sa.VARCHAR(length=40), autoincrement=False, nullable=True),
    sa.Column('strava_athlete_info', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key'),
    sa.UniqueConstraint('strava_id', name='user_strava_id_key'),
    sa.UniqueConstraint('username', name='user_username_key')
    )
    op.drop_table('users')
    # ### end Alembic commands ###