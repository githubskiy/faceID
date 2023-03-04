"""newwwww_

Revision ID: e3418eec0e2d
Revises: 8e2963d98259
Create Date: 2023-03-04 16:03:31.274248

"""
from alembic import op
import sqlalchemy as sa
import pgvector

# revision identifiers, used by Alembic.
revision = 'e3418eec0e2d'
down_revision = '8e2963d98259'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('path_storage', sa.String(), nullable=True),
    sa.Column('face_embeding', pgvector.sqlalchemy.Vector(dim=128), nullable=True),
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
