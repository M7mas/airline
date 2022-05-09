"""changing cloumn to col

Revision ID: c45374282041
Revises: bdd63c3f9886
Create Date: 2022-05-07 16:22:51.795921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c45374282041'
down_revision = 'bdd63c3f9886'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('seats', sa.Column('row', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###