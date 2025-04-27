"""remove preferred task types

Revision ID: b2c3d4e5
Revises: a1b2c3d4
Create Date: 2024-04-27 11:14:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b2c3d4e5'
down_revision = 'a1b2c3d4'
branch_labels = None
depends_on = None

def upgrade():
    # Drop preferred_task_types column
    op.drop_column('publishers', 'preferred_task_types')

def downgrade():
    # Add preferred_task_types column back
    op.add_column('publishers', sa.Column('preferred_task_types', sa.JSON(), nullable=True)) 