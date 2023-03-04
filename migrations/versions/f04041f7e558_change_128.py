"""change_128

Revision ID: f04041f7e558
Revises: b6b3ef951fb7
Create Date: 2023-03-01 23:27:05.426177

"""
from alembic import op
import sqlalchemy as sa
import pgvector

# revision identifiers, used by Alembic.
revision = 'f04041f7e558'
down_revision = 'b6b3ef951fb7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
