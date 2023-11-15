"""in3

Revision ID: 2986c8d845cc
Revises: 561693009f02
Create Date: 2023-11-09 19:02:31.309993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2986c8d845cc'
down_revision = '561693009f02'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('url_map', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.drop_index('ix_url_map_timestamppp', table_name='url_map')
    op.create_index(op.f('ix_url_map_timestamp'), 'url_map', ['timestamp'], unique=False)
    op.drop_column('url_map', 'timestamppp')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('url_map', sa.Column('timestamppp', sa.DATETIME(), nullable=True))
    op.drop_index(op.f('ix_url_map_timestamp'), table_name='url_map')
    op.create_index('ix_url_map_timestamppp', 'url_map', ['timestamppp'], unique=False)
    op.drop_column('url_map', 'timestamp')
    # ### end Alembic commands ###