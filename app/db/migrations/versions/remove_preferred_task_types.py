"""remove preferred task types

Revision ID: remove_preferred_task_types
Revises: add_preferred_task_types
Create Date: 2024-04-27 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision = 'remove_preferred_task_types'
down_revision = 'add_preferred_task_types'
branch_labels = None
depends_on = None

def upgrade():
    op.drop_column('publishers', 'preferred_task_types')

def downgrade():
    op.add_column('publishers', sa.Column('preferred_task_types', JSON, nullable=False, server_default='[]')) 