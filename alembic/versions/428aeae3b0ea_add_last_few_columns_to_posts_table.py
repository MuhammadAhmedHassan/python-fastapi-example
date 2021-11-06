"""add last few columns to posts table

Revision ID: 428aeae3b0ea
Revises: f6f897370661
Create Date: 2021-11-06 12:54:01.840554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '428aeae3b0ea'
down_revision = 'f6f897370661'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'
    ))
    op.add_column("posts", sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')
    ))
    op.add_column("posts", sa.Column(
        'updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'), onupdate=sa.text('NOW()')
    ))
    pass


def downgrade():
    op.drop_column(table_name="posts", column_name="published")
    op.drop_column(table_name="posts", column_name="created_at")
    op.drop_column(table_name="posts", column_name="updated_at")
    pass
