"""add content column to posts table

Revision ID: e108850f5420
Revises: 90c93a6207f5
Create Date: 2023-06-19 21:20:46.077791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e108850f5420'
down_revision = '90c93a6207f5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
