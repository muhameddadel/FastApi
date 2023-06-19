"""add columns to posts table

Revision ID: db5e49e1bb41
Revises: 55af3ad089be
Create Date: 2023-06-19 22:30:12.831158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db5e49e1bb41'
down_revision = '55af3ad089be'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE")) 
    op.add_column("posts", sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))



def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
