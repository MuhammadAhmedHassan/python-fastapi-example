"""add foreign key to posts table

Revision ID: f6f897370661
Revises: d4b5abfc705d
Create Date: 2021-11-06 12:47:21.323968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6f897370661'
down_revision = 'd4b5abfc705d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', 
        source_table="posts", referent_table="users", 
        local_cols=["owner_id"], remote_cols=['id'],
        ondelete='CASCADE'
    )
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column(table_name='posts', column_name='owner_id')
    pass
