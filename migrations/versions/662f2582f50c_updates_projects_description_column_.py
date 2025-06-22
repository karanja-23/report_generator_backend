"""Updates Projects description column type to JSON

Revision ID: 662f2582f50c
Revises: ad8db06265fc
Create Date: 2025-06-22 01:00:10.407042
"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = '662f2582f50c'
down_revision = 'ad8db06265fc'
branch_labels = None
depends_on = None

def upgrade():
    # Use raw SQL to cast existing VARCHAR to JSON
    op.execute("""
        ALTER TABLE projects
        ALTER COLUMN description
        TYPE JSON
        USING description::json
    """)

def downgrade():
    # Revert JSON column back to VARCHAR(255)
    op.execute("""
        ALTER TABLE projects
        ALTER COLUMN description
        TYPE VARCHAR(255)
        USING description::text
    """)
