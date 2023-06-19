"""add foregin key to posts table

Revision ID: 55af3ad089be
Revises: 45ae5f8056ff
Create Date: 2023-06-19 21:32:06.759754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55af3ad089be'
down_revision = '45ae5f8056ff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk", source_table="posts", referent_table="users", 
                            local_cols=["user_id"], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
