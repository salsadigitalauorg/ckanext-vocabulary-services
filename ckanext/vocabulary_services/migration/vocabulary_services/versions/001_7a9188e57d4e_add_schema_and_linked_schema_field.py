"""Add schema and linked schema field

Revision ID: 7a9188e57d4e
Revises: 
Create Date: 2021-12-01 00:26:06.778970

"""
from alembic import op
import sqlalchemy as sa
import datetime
# revision identifiers, used by Alembic.
revision = '7a9188e57d4e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    engine = op.get_bind()
    inspector = sa.inspect(engine)
    tables = inspector.get_table_names()
    if 'vocabulary_service' not in tables:
        op.create_table(
            'vocabulary_service',
            sa.Column('id', sa.String, primary_key=True),
            sa.Column('type', sa.String, nullable=False),
            sa.Column('title', sa.String, nullable=False),
            sa.Column('name', sa.String, nullable=False, unique=True),
            sa.Column('schema', sa.String, nullable=False),
            sa.Column('linked_schema_field', sa.String, nullable=False),
            sa.Column('uri', sa.String, nullable=False),
            sa.Column('update_frequency', sa.String, nullable=False),
            sa.Column('allow_duplicate_terms', sa.Boolean, default=False),
            sa.Column('is_hierarchical', sa.Boolean, default=False),
            sa.Column('date_created', sa.DateTime, default=datetime.datetime.utcnow()),
            sa.Column('date_modified', sa.DateTime, default=datetime.datetime.utcnow()),
            sa.Column('date_last_processed', sa.DateTime)
        )

        if 'vocabulary_service_term' not in tables:
            op.create_table(
                'vocabulary_service_term',
                sa.Column('id', sa.String, primary_key=True),
                sa.Column('vocabulary_service_id', sa.String, sa.ForeignKey('vocabulary_service.id'), nullable=False),
                sa.Column('term', sa.String, nullable=False),
                sa.Column('uri', sa.String, nullable=False),
                sa.Column('description', sa.String, nullable=True),
                sa.Column('parent_id', sa.String, sa.ForeignKey('vocabulary_service_term.id'), nullable=True),
                sa.Column('quantity_kind', sa.String, nullable=True),
                sa.Column('date_created', sa.DateTime, default=datetime.datetime.utcnow()),
                sa.Column('date_modified', sa.DateTime, default=datetime.datetime.utcnow())
            )

def downgrade():
    op.drop_table('vocabulary_service_term')
    op.drop_table('vocabulary_service')
