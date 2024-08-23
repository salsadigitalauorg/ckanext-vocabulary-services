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
    # Add column with nullable = True.
    op.add_column('vocabulary_service', sa.Column('schema', sa.UnicodeText, nullable=True))
    op.add_column('vocabulary_service', sa.Column('linked_schema_field', sa.UnicodeText, nullable=True))

    # Add default value to all null columns.
    dummy_null_query = 'update vocabulary_service set schema = \' \'; update vocabulary_service set linked_schema_field = \' \'; '
    op.execute(dummy_null_query)

    # Set the column to nullable = False.
    op.alter_column('vocabulary_service', 'schema', nullable=False)
    op.alter_column('vocabulary_service', 'linked_schema_field', nullable=False)


def downgrade():
    op.drop_column('vocabulary_service', 'schema')
    op.drop_column('vocabulary_service', 'linked_schema_field')
