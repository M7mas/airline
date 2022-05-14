"""cascade order

Revision ID: 29c6036d4238
Revises: 8357cdc981ad
Create Date: 2022-05-14 15:31:19.934999

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29c6036d4238'
down_revision = '8357cdc981ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('orders_ticket_id_fkey', 'orders', type_='foreignkey')
    op.create_foreign_key(None, 'orders', 'tickets', ['ticket_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.create_foreign_key('orders_ticket_id_fkey', 'orders', 'tickets', ['ticket_id'], ['id'], ondelete='RESTRICT')
    # ### end Alembic commands ###
