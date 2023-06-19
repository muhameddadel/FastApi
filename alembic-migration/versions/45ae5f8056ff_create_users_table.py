"""create users table

Revision ID: 45ae5f8056ff
Revises: e108850f5420
Create Date: 2023-06-19 21:22:57.681345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45ae5f8056ff'
down_revision = 'e108850f5420'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", sa.Column('id', sa.Integer(), primary_key=True,nullable=False),
                            sa.Column('email', sa.String(), unique=True,nullable=False),
                            sa.Column('password', sa.String(), nullable=False),
                            sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
                            )

def downgrade() -> None:
    op.drop_table("users")
