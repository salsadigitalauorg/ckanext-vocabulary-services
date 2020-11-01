"""Add allow_duplicate_terms column

Revision ID: 8316ab08511a
Revises: 3ae4b17ed66d
Create Date: 2020-11-01 20:16:51.488570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8316ab08511a'
down_revision = '3ae4b17ed66d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('vocabulary_service', sa.Column('allow_duplicate_terms', sa.Boolean, server_default='FALSE'))


def downgrade():
    op.drop_column('vocabulary_service', 'allow_duplicate_terms')
