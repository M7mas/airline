"""row int -> str

Revision ID: bdd63c3f9886
Revises: 590b58243281
Create Date: 2022-05-07 16:20:18.783432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdd63c3f9886'
down_revision = '590b58243281'
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
