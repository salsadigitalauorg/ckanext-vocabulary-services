"""Add definition to vocabulary_service_term

Revision ID: 26af172f336f
Revises: 8316ab08511a
Create Date: 2020-11-05 00:29:05.890072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26af172f336f'
down_revision = '8316ab08511a'
branch_labels = None
depends_on = None


def upgrade():
     op.add_column('vocabulary_service_term', sa.Column('definition', sa.UnicodeText))


def downgrade():
    op.drop_column('vocabulary_service_term', 'definition')
