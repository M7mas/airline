"""creating a temp table

Revision ID: d8d253e0371d
Revises: b4561b5d13da
Create Date: 2022-05-02 01:31:34.987489

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision = 'd8d253e0371d'
down_revision = 'b4561b5d13da'
branch_labels = None
depends_on = None


def upgrade():
    pass

def downgrade():
    pass    
