# To create this type of file
# alembic revision -m "add content column to posts table"
"""create posts table

Revision ID: 7a823353edd1
Revises: 
Create Date: 2021-11-06 12:31:47.481280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a823353edd1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False)
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
