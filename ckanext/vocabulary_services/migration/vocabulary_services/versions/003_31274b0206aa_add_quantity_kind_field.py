"""empty message

Revision ID: 31274b0206aa
Revises: cdce2303c1ec
Create Date: 2024-08-19 19:44:40.843957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31274b0206aa'
down_revision = 'cdce2303c1ec'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('vocabulary_service_term', sa.Column('quantity_kind', sa.UnicodeText, nullable=True))


def downgrade():
    op.drop_column('vocabulary_service_term', 'quantity_kind')