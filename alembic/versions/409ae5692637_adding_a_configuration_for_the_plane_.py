"""adding a configuration for the plane type

Revision ID: 409ae5692637
Revises: 55d43dc842f4
Create Date: 2022-05-07 09:54:49.228406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '409ae5692637'
down_revision = '55d43dc842f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('types', sa.Column('configuration_seat_FirstClass', sa.Integer(), nullable=False))
    op.add_column('types', sa.Column('configuration_seat_Business', sa.Integer(), nullable=False))
    op.add_column('types', sa.Column('configuration_seat_PremiumEconomy', sa.Integer(), nullable=False))
    op.add_column('types', sa.Column('configuration_seat_Economy', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('types', 'configuration_seat_Economy')
    op.drop_column('types', 'configuration_seat_PremiumEconomy')
    op.drop_column('types', 'configuration_seat_Business')
    op.drop_column('types', 'configuration_seat_FirstClass')
    # ### end Alembic commands ###
