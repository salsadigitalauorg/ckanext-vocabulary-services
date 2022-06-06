"""Add data_type column

Revision ID: 8efb2a4d3a5a
Revises: cdce2303c1ec
Create Date: 2022-06-06 16:18:52.466288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8efb2a4d3a5a'
down_revision = 'cdce2303c1ec'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('vocabulary_service', sa.Column('data_type', sa.UnicodeText, nullable=True))


def downgrade():
    op.drop_column('vocabulary_service', 'quantity_kind')