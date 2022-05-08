"""setting up DB for Air Line tables

Revision ID: 71cd7b316966
Revises: 73177618ef56
Create Date: 2022-05-05 07:21:43.909488

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '71cd7b316966'
down_revision = '73177618ef56'
branch_labels = None
depends_on = None

def upgrade():
    pass

def downgrade():
    pass