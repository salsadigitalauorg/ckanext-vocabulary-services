"""Add schema and linked schema field

Revision ID: 7a9188e57d4e
Revises: 
Create Date: 2021-12-01 00:26:06.778970

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7a9188e57d4e'
down_revision = None
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
