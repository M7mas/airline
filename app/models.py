from email.policy import default
from enum import unique
from xmlrpc.client import DateTime
from psycopg2 import Timestamp
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import DateTime
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import foreign
from sqlalchemy.sql.schema import ForeignKey
# This class represent each table on the DataBase.


class Temp(Base):
    __tablename__ = "post"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    private = Column(Boolean, server_default='False')
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text('current_timestamp(0)'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text('current_timestamp(0)'))
    phone_number = Column(String, nullable=True)



# This for the Actual Project
# to get YYYY-MM-DD HH:MM:SS+XX -> 'current_timestamp(0)'


