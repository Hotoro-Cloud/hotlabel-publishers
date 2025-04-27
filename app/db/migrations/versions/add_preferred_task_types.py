"""add preferred task types

Revision ID: add_preferred_task_types
Revises: previous_revision
Create Date: 2024-03-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision = 'add_preferred_task_types'
down_revision = 'previous_revision'  # Update this to your previous migration
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('publishers', sa.Column('preferred_task_types', JSON, nullable=False, server_default='[]'))

def downgrade():
    op.drop_column('publishers', 'preferred_task_types') 