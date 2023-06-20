"""auto-vote

Revision ID: ff53eab3ca52
Revises: db5e49e1bb41
Create Date: 2023-06-19 23:14:43.635719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff53eab3ca52'
down_revision = 'db5e49e1bb41'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###