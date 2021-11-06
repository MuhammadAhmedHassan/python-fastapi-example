"""add content column to posts table

Revision ID: 3ef507dd750a
Revises: 7a823353edd1
Create Date: 2021-11-06 12:36:40.497201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ef507dd750a'
down_revision = '7a823353edd1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column('content', sa.String(), nullable=False)
    )
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
