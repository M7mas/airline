"""create user table

Revision ID: b4561b5d13da
Revises: 
Create Date: 2022-05-02 01:21:27.656841

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision = 'b4561b5d13da'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=text('current_timestamp(0)'))
        
        # id = Column(Integer, primary_key=True, nullable=False)
        # email = Column(String, nullable=False, unique=True)
        # password = Column(String, nullable=False)
        # created_at = Column(DateTime(timezone=True), nullable=False, server_default=text('current_timestamp(0)'))
    )
    


def downgrade():
    op.drop_table('users')
    
