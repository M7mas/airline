from email.policy import default
from enum import unique
from time import timezone
from xmlrpc.client import DateTime
from psycopg2 import Timestamp
from sqlalchemy import Column, Integer, String, Boolean, null
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import DateTime, Date, Time
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import foreign
from sqlalchemy.sql.schema import ForeignKey
# This class represent each table on the DataBase.


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    # username = Column(String, nullable=False, unique=True) # There is no need for this right now
    fname = Column(String, nullable=False)
    mname = Column(String, nullable=True)
    lname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    dateofbirth = Column(Date, nullable=False)
    role = Column(String, server_default='user', nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text('current_timestamp(0)'))
    phone_number = Column(String, nullable=True)

class Blacklist(Base):
    __tablename__ = "blacklist"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False, unique=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    
    user = relationship("User")

class Admin(Base):
    __tablename__ = "admins"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False, unique=True)
    salary = Column(Integer, nullable=False)
    
    user = relationship("User")

class Passenger(Base):
    __tablename__ = "passengers"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False, unique=True)
    points = Column(Integer, nullable=False)
    
    user = relationship("User")

class Card(Base):
    __tablename__ = "cards"
    
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    number = Column(String, nullable=False)
    name = Column(String, nullable=False)
    
    user = relationship("User")

class WaitList(Base):
    __tablename__ = "waitlist"
    
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id", ondelete="CASCADE"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    
    tclass = relationship("TClass", foreign_keys=[class_id])
    user = relationship("User", foreign_keys=[user_id])
    flight = relationship("Flight", foreign_keys=[flight_id])

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, nullable=False)
    fname = Column(String, nullable=False)
    mname = Column(String, nullable=True)
    lname = Column(String, nullable=False)
    serial = Column(String(length=1), nullable=False)
    expiredate = Column(Date, nullable=False)
    ordered_at = Column(DateTime(timezone=True), nullable=False, server_default=text('current_timestamp(0)'))
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id", ondelete="CASCADE"), nullable=False)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="RESTRICT"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False)
    state_id = Column(Integer, ForeignKey("states.id", ondelete="CASCADE"), nullable=False)
    
    state = relationship("State", foreign_keys=[state_id])
    user = relationship("User", foreign_keys=[user_id])
    flight = relationship("Flight", foreign_keys=[flight_id])
    ticket = relationship("Ticket", foreign_keys=[ticket_id])
    card = relationship("Card", foreign_keys=[card_id])

class Weight(Base):
    __tablename__ = "weights"
    
    id = Column(Integer, primary_key=True, nullable=False)
    weight = Column(String, nullable=False)

class State(Base):
    __tablename__ = "states"
    
    id = Column(Integer, primary_key=True, nullable=False)
    state = Column(String, nullable=False)

class TClass(Base):
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True, nullable=False)
    classes = Column(String, nullable=False)

class Seat(Base):
    __tablename__ = "seats"
    
    id = Column(Integer, primary_key=True, nullable=False)
    rows = Column(String, nullable=False)
    cols = Column(String, nullable=False)


class Price(Base):
    __tablename__ = "prices"
    
    id = Column(Integer, primary_key=True, nullable=False)
    price = Column(Integer, nullable=False)



class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, nullable=False)
    time = Column(Time(timezone=False), nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id", ondelete="CASCADE"), nullable=False)
    weight_id = Column(Integer, ForeignKey("weights.id", ondelete="CASCADE"), nullable=False)
    state_id = Column(Integer, ForeignKey("states.id", ondelete="CASCADE"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id", ondelete="CASCADE"), nullable=False)
    price_id = Column(Integer, ForeignKey("prices.id", ondelete="CASCADE"), nullable=False)

    flight = relationship("Flight", foreign_keys=[flight_id])
    weight = relationship("Weight", foreign_keys=[weight_id])
    state = relationship("State", foreign_keys=[state_id])
    tclass = relationship("TClass", foreign_keys=[class_id])
    seat = relationship("Seat", foreign_keys=[seat_id])
    price = relationship("Price", foreign_keys=[price_id])


class Flight(Base):
    __tablename__ = "flights"
    
    id = Column(Integer, primary_key=True, nullable=False)
    source_city = Column(String, nullable=False)
    destination_city = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    
    state_id = Column(Integer, ForeignKey("states.id", ondelete="CASCADE"), nullable=False)
    plane_id = Column(Integer, ForeignKey("planes.id", ondelete="CASCADE"), nullable=False)
    
    state = relationship("State", foreign_keys=[state_id])
    plane = relationship("Plane", foreign_keys=[plane_id])


class Plane(Base):
    __tablename__ = "planes"
    
    id = Column(Integer, primary_key=True, nullable=False)
    type_id = Column(Integer, ForeignKey("types.id", ondelete="CASCADE"), nullable=False)

    type = relationship("Type", foreign_keys=[type_id])



class Maintenance(Base):
    __tablename__ = "maintentaces"
    
    id = Column(Integer, primary_key=True, nullable=False)
    last_date = Column(Date, nullable=False)
    next_date = Column(Date, nullable=False)
    plane_id = Column(Integer, ForeignKey("planes.id", ondelete="CASCADE"), nullable=False)
    
    plane = relationship("Plane", foreign_keys=[plane_id])


class Type(Base):
    __tablename__ = "types"
    
    id = Column(Integer, primary_key=True, nullable=False)
    model = Column(String, nullable=False)
    name = Column(String, nullable=False)
    engine = Column(String, nullable=False)
    max_speed = Column(Integer, nullable=False)
    number_engine = Column(Integer, nullable=False)
    configuration_seat_FirstClass = Column(Integer, nullable=False)
    configuration_seat_Business = Column(Integer, nullable=False)
    configuration_seat_PremiumEconomy = Column(Integer, nullable=False)
    configuration_seat_Economy = Column(Integer, nullable=False)
    number_seat_FirstClass = Column(Integer, nullable=False)
    number_seat_Business = Column(Integer, nullable=False)
    number_seat_PremiumEconomy = Column(Integer, nullable=False)
    number_seat_Economy = Column(Integer, nullable=False)


class Fine(Base):
    __tablename__ = "fines"
    
    flight_id = Column(Integer, ForeignKey("flights.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    amount = Column(Integer, nullable=False)
    state_id = Column(Integer, ForeignKey("states.id", ondelete="CASCADE"), nullable=False)
    
    flight = relationship("Flight", foreign_keys=[flight_id])
    state = relationship("State", foreign_keys=[state_id])
    


# This for the Actual Project
# to get YYYY-MM-DD HH:MM:SS+XX -> 'current_timestamp(0)'


