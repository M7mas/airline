"""adding fk to temp

Revision ID: bf08b9d1b4dd
Revises: d8d253e0371d
Create Date: 2022-05-02 01:41:24.906058

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision = 'bf08b9d1b4dd'
down_revision = 'd8d253e0371d'
branch_labels = None
depends_on = None


def upgrade():
    pass
    


def downgrade():
    pass