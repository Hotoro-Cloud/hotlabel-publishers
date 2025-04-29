"""convert publisher id to uuid

Revision ID: convert_publisher_id_to_uuid
Revises: b2c3d4e5
Create Date: 2024-04-28 04:25:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision = 'convert_publisher_id_to_uuid'
down_revision = 'b2c3d4e5'
branch_labels = None
depends_on = None

def upgrade():
    # Create a new UUID column
    op.add_column('publishers', sa.Column('new_id', UUID(), nullable=True))
    
    # Create a function to convert string ID to UUID
    op.execute("""
    CREATE OR REPLACE FUNCTION extract_uuid_from_pub_id(pub_id text) 
    RETURNS uuid AS $$
    DECLARE
        uuid_str text;
    BEGIN
        -- Extract the hex part after 'pub_' and pad it to full UUID length
        uuid_str := substring(pub_id from 5) || repeat('0', 24);
        RETURN uuid_str::uuid;
    EXCEPTION WHEN OTHERS THEN
        -- If conversion fails, generate a new UUID
        RETURN gen_random_uuid();
    END;
    $$ LANGUAGE plpgsql;
    """)
    
    # Convert existing IDs
    op.execute("""
    UPDATE publishers 
    SET new_id = extract_uuid_from_pub_id(id)
    WHERE new_id IS NULL;
    """)
    
    # Drop the function as it's no longer needed
    op.execute("DROP FUNCTION extract_uuid_from_pub_id(text);")
    
    # Make new_id not nullable
    op.alter_column('publishers', 'new_id', nullable=False)
    
    # Drop the old id column and rename new_id to id
    op.drop_column('publishers', 'id')
    op.alter_column('publishers', 'new_id', new_column_name='id')
    
    # Add primary key constraint
    op.create_primary_key('pk_publishers', 'publishers', ['id'])
    op.create_index(op.f('ix_publishers_id'), 'publishers', ['id'], unique=True)

def downgrade():
    # Create a new string column
    op.add_column('publishers', sa.Column('old_id', sa.String(), nullable=True))
    
    # Convert UUIDs back to string format
    op.execute("""
    UPDATE publishers 
    SET old_id = 'pub_' || substring(id::text from 1 for 8)
    WHERE old_id IS NULL;
    """)
    
    # Make old_id not nullable
    op.alter_column('publishers', 'old_id', nullable=False)
    
    # Drop the UUID id column and rename old_id to id
    op.drop_column('publishers', 'id')
    op.alter_column('publishers', 'old_id', new_column_name='id')
    
    # Add primary key constraint
    op.create_primary_key('pk_publishers', 'publishers', ['id'])
    op.create_index(op.f('ix_publishers_id'), 'publishers', ['id'], unique=True) 