"""update publisher fields

Revision ID: a1b2c3d4
Revises: 41265e8980b7
Create Date: 2024-04-27 11:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a1b2c3d4'
down_revision = '41265e8980b7'
branch_labels = None
depends_on = None

def upgrade():
    # Rename columns
    op.alter_column('publishers', 'company_name', new_column_name='name')
    op.alter_column('publishers', 'website_url', new_column_name='website')
    op.alter_column('publishers', 'contact_email', new_column_name='email')
    
    # Add description column
    op.add_column('publishers', sa.Column('description', sa.String(), nullable=True))

def downgrade():
    # Drop description column
    op.drop_column('publishers', 'description')
    
    # Rename columns back
    op.alter_column('publishers', 'name', new_column_name='company_name')
    op.alter_column('publishers', 'website', new_column_name='website_url')
    op.alter_column('publishers', 'email', new_column_name='contact_email') 