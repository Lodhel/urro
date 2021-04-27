"""roreestr

Revision ID: 7fd13da343e0
Revises: 
Create Date: 2021-04-27 21:59:08.698242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fd13da343e0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'debtor',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('debtor', sa.String(200), nullable=True),
        sa.Column('status_order', sa.String(200), nullable=True),
        sa.Column('query_num', sa.String(200), nullable=True)
    )

def downgrade():
    pass
