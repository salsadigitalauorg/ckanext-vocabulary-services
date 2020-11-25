"""Add columns to vocab service and term

Revision ID: 94c4b4dc84db
Revises: 26af172f336f
Create Date: 2020-11-19 07:29:45.066439

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '94c4b4dc84db'
down_revision = '26af172f336f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('vocabulary_service', sa.Column('is_hierarchical', sa.Boolean, default=False))
    op.add_column('vocabulary_service_term', sa.Column('broader', sa.UnicodeText, nullable=True))


def downgrade():
    op.drop_column('vocabulary_service', 'is_hierarchical')
    op.drop_column('vocabulary_service_term', 'broader')
