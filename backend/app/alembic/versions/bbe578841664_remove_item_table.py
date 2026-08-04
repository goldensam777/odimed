"""remove_item_table

Revision ID: bbe578841664
Revises: 768ea0eebfe1
Create Date: 2026-08-04 12:37:37.940237

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'bbe578841664'
down_revision = '768ea0eebfe1'
branch_labels = None
depends_on = None


def upgrade():
    # Suppression explicite de la table item si elle existe
    op.execute("DROP TABLE IF EXISTS item CASCADE;")


def downgrade():
    pass
