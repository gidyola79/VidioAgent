"""add password_hash to businesses

Revision ID: add_password_hash_businesses
Revises: 8678dbaf16e5
Create Date: 2025-12-17 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_password_hash_businesses'
down_revision = '8678dbaf16e5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('businesses', sa.Column('password_hash', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('businesses', 'password_hash')
