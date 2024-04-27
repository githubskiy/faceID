"""create_table4

Revision ID: 0bfb7b629a67
Revises: 8b83d0e070c1
Create Date: 2023-05-31 19:28:05.314042

"""
from alembic import op
import sqlalchemy as sa
import pgvector

# revision identifiers, used by Alembic.
revision = '0bfb7b629a67'
down_revision = '8b83d0e070c1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('path_storage', sa.String(), nullable=True),
    sa.Column('face_embeding', pgvector.sqlalchemy.Vector(dim=512), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###