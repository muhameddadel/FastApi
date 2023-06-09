"""create posts table

Revision ID: 90c93a6207f5
Revises: 
Create Date: 2023-06-19 18:47:01.099425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90c93a6207f5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                            sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
