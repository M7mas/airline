"""adding a fines table -> flight's canceled or delayed

Revision ID: 026bbc663549
Revises: ec274e42e85d
Create Date: 2022-05-07 04:25:23.589756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '026bbc663549'
down_revision = 'ec274e42e85d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fines',
    sa.Column('flight_id', sa.Integer(), nullable=False),
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['flight_id'], ['flights.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['state_id'], ['states.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('flight_id')
    )
    op.create_unique_constraint(None, 'admins', ['user_id'])
    op.create_unique_constraint(None, 'blacklist', ['user_id'])
    op.create_unique_constraint(None, 'passengers', ['user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'passengers', type_='unique')
    op.drop_constraint(None, 'blacklist', type_='unique')
    op.drop_constraint(None, 'admins', type_='unique')
    op.drop_table('fines')
    # ### end Alembic commands ###
