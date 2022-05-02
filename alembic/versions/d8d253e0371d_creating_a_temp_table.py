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
    op.create_table(
        'Temp',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('content', sa.String, nullable=False),
        sa.Column('private', sa.Boolean, server_default='False'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=text('current_timestamp(0)'))
    )
    
    # id = Column(Integer, primary_key=True, nullable=False)
    # title = Column(String, nullable=False)
    # content = Column(String, nullable=False)
    # private = Column(Boolean, server_default='False')
    # created_at = Column(DateTime(timezone=True), nullable=False, server_default=text('current_timestamp(0)'))



def downgrade():
    op.drop_table('Temp')
    
