"""add quantity_kind field

Revision ID: cdce2303c1ec
Revises: 7a9188e57d4e
Create Date: 2021-12-04 13:19:08.780918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdce2303c1ec'
down_revision = '7a9188e57d4e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('vocabulary_service_term', sa.Column('quantity_kind', sa.UnicodeText, nullable=True))


def downgrade():
    op.drop_column('vocabulary_service_term', 'quantity_kind')
