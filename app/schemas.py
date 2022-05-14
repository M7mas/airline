from datetime import date, datetime, time
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# This class responsible for handling ->/<- the API.
# request to the API
# response from the API
# responses must have Config class

######################################################## --- Else-Models --- ##############################################

# This model just an empty for response and request w/
# configuration -> orm_mode/ alias name.
class Model(BaseModel): # to inherate from it w/out configuring each and every class
    class Config:
        orm_mode = True
        allow_population_by_field_name = True # This just for the usage of alias.
class TokenData(BaseModel):
    id: Optional[str] = None




######################################################## --- Request --- ##############################################
class TokenREQ(BaseModel):
    access_token: str
    token_type: str

# This class for the user to sign up:
class UserSignUpREQ(Model):
    
    email: EmailStr = Field(alias="Email")
    fname: str = Field(alias="First_Name")
    mname: Optional[str] = Field(alias="Middle_Name")
    lname: str = Field(alias="Last_Name")
    password: str = Field(alias="Password")
    dateofbirth: date = Field(alias="Date_of_Birth")
    phone_number: Optional[str] = Field(alias="Phone_Number")

class UserUpdateREQ(Model):
    
    email: Optional[EmailStr] = Field(alias="Email")
    fname: Optional[str] = Field(alias="First_Name")
    mname: Optional[str] = Field(alias="Middle_Name")
    lname: Optional[str] = Field(alias="Last_Name")
    password: Optional[str] = Field(alias="Password")
    dateofbirth: Optional[date] = Field(alias="Date_of_Birth")
    phone_number: Optional[str] = Field(alias="Phone_Number")

class UserUpdateRoleREQ(Model):
    role: Optional[str]
class CardsREQ(Model):
    user_id: int = 0
    type: str
    number: str
    name: str
class CardUpdateREQ(Model):
    user_id: Optional[int] = 0
    type: Optional[str]
    number: Optional[str]
    name: Optional[str]

class BlackListREQ(Model):
    user_id: int
    title: str
    description: str

class BlackListUpdateREQ(Model):
    user_id: Optional[int]
    title: Optional[str]
    description: Optional[str]

class ClassREQ(Model):
    classes: str

class StateREQ(Model):
    state: str

class TypeREQ(Model):
    model: str  = Field(alias="model")
    name: str  = Field(alias="name")
    engine: str  = Field(alias="engine model")
    max_speed: int  = Field(alias="Maximum Speed")
    number_engine: int  = Field(alias="number of engines")
    configuration_seat_FirstClass: int  = Field(alias="number of seats per column for First Class")
    configuration_seat_Business: int  = Field(alias="number of seats per column for Business Class")
    configuration_seat_PremiumEconomy: int  = Field(alias="number of seats per column for PremiumEconomy Class")
    configuration_seat_Economy: int  = Field(alias="number of seats per column for Economy Class")
    number_seat_FirstClass: int  = Field(alias="number of seats for First Class")
    number_seat_Business: int  = Field(alias="number of seats for Business Class")
    number_seat_PremiumEconomy: int  = Field(alias="number of seats for PremiumEconomy Class")
    number_seat_Economy: int  = Field(alias="number of seats for Economy Class")

class TypeUpdateREQ(Model):
    model: Optional[str]  = Field(alias="model")
    name: Optional[str]  = Field(alias="name")
    engine: Optional[str]  = Field(alias="engine model")
    max_speed: Optional[int]  = Field(alias="Maximum Speed")
    number_engine: Optional[int]  = Field(alias="number of engines")
    configuration_seat_FirstClass: Optional[int]  = Field(alias="number of seats per column for First Class")
    configuration_seat_Business: Optional[int]  = Field(alias="number of seats per column for Business Class")
    configuration_seat_PremiumEconomy: Optional[int]  = Field(alias="number of seats per column for PremiumEconomy Class")
    configuration_seat_Economy: Optional[int]  = Field(alias="number of seats per column for Economy Class")
    number_seat_FirstClass: Optional[int]  = Field(alias="number of seats for First Class")
    number_seat_Business: Optional[int]  = Field(alias="number of seats for Business Class")
    number_seat_PremiumEconomy: Optional[int]  = Field(alias="number of seats for PremiumEconomy Class")
    number_seat_Economy: Optional[int]  = Field(alias="number of seats for Economy Class")

class PlaneREQ(Model):
    type_id: int

class FlightREQ(Model):
    source_city: str
    destination_city: str
    date: date
    state_id: int
    plane_id: int

class FlightUpdateREQ(Model):
    source_city: Optional[str]
    destination_city: Optional[str]
    date: Optional[date]
    state_id: Optional[int]
    plane_id: Optional[int]

class FineREQ(Model):
    flight_id: int
    amount: int
    state_id: int

class FineUpdateREQ(Model):
    flight_id: int = 0
    amount: Optional[int]
    state_id: Optional[int]


class SeatREQ(Model):
    rows: str
    cols: str

class SeatUpdateREQ(Model):
    id: int = 0
    rows: Optional[str]
    cols: Optional[str]

class WeightREQ(Model):
    weight: str


class PriceREQ(Model):
    price: int

class MaintenanceREQ(Model):
    last_date: date
    next_date: date
    plane_id: int

class MaintenanceUpdateREQ(Model):
    last_date: Optional[date]
    next_date: Optional[date]
    plane_id: Optional[int]



class WaitListREQ(Model):
    user_id: int
    flight_id: int
    class_id: int

class WaitListUpdateREQ(Model):
    user_id: Optional[int]
    flight_id: Optional[int]
    class_id: Optional[int]

class TicketREQ(Model):
    time: time
    flight_id: int
    weight_id: int
    state_id: int = 3
    class_id: int
    seat_id: int
    price_id: int

class TicketUpdateREQ(Model):
    time: Optional[time]
    weight_id: Optional[int]
    state_id: Optional[int]
    class_id: Optional[int]
    price_id: Optional[int]



class OrderREQ(Model):
    fname: str
    mname:  Optional[str]
    lname: str
    user_id: Optional[int]
    ticket_id: int
    card_id: int

class OrderUpdateREQ(Model):
    fname: Optional[str]
    mname:  Optional[str]
    lname: Optional[str]

class OrderDeleteREQ(Model):
    class_id: Optional[int]


class MakingAdminREQ(Model):
    user_id: Optional[int]
    salary: Optional[int]

class TicketUpdateState(Model):
    state_id: Optional[int]

######################################################## --- Response --- ##############################################
# This for passengers
class PassengerRES(Model):
    user_id: int = Field(alias="Identification")
    points: int = Field(alias="Points")

# This class is response for UserSignUp
class UserSignUpRES(Model):
    id: int = Field(alias="Identification")
    email: EmailStr = Field(alias="Email")
    fname: str = Field(alias="First_Name")
    mname: Optional[str] = Field(alias="Middle_Name")
    lname: str = Field(alias="Last_Name")
    phone_number: Optional[str] = Field(alias="Phone_Number")


class CardsRES(Model):
    id: int
    type: str
    number: str
    name: str

class BlackListRES(Model):
    title: str
    description: Optional[str]
    user: UserSignUpRES

class ClassRES(Model):
    id: int
    classes: str

class StateRES(Model):
    id: int
    state: str


class TypeRES(Model):
    id: str  = Field(alias="Identification")
    model: str  = Field(alias="model")
    name: str  = Field(alias="name")
    engine: str  = Field(alias="engine model")
    max_speed: int  = Field(alias="Maximum Speed")
    number_engine: int  = Field(alias="number of engines")
    configuration_seat_FirstClass: int  = Field(alias="number of seats per column for First Class")
    configuration_seat_Business: int  = Field(alias="number of seats per column for Business Class")
    configuration_seat_PremiumEconomy: int  = Field(alias="number of seats per column for PremiumEconomy Class")
    configuration_seat_Economy: int  = Field(alias="number of seats per column for Economy Class")
    number_seat_FirstClass: int  = Field(alias="number of seats for First Class")
    number_seat_Business: int  = Field(alias="number of seats for Business Class")
    number_seat_PremiumEconomy: int  = Field(alias="number of seats for PremiumEconomy Class")
    number_seat_Economy: int  = Field(alias="number of seats for Economy Class")


class PlaneRES(Model):
    id: int
    type: TypeRES


class FlightRES(Model):
    id: int
    source_city: str
    destination_city: str
    date: date
    state: StateRES
    plane: PlaneRES


class FineRES(Model):
    amount: int
    flight: FlightRES
    state: StateRES


class SeatRES(Model):
    id: int
    rows: str
    cols: str


class WeightRES(Model):
    id: int
    weight: str



class PriceRES(Model):
    id: int
    price: int

class MaintenanceRES(Model):
    id: int
    last_date: date
    next_date: date
    plane: PlaneRES

class WaitListRES(Model):
    id: int
    tclass: ClassRES = Field(alias="class")
    user: UserSignUpRES
    flight: FlightRES


class TicketRES(Model):
    id: int
    flight: FlightRES
    time: time
    weight: WeightRES
    state: StateRES
    tclass: ClassRES = Field(alias="class")
    seat: SeatRES
    price: PriceRES

class OrderRES(Model):
    id: int
    serial: str
    expiredate: date
    ordered_at: datetime
    
    user: UserSignUpRES
    ticket: TicketRES
    state: StateRES
    card: CardsRES

# in order to use alias ->
# after the type : "= Field(alias="The_Name")"
# exp.:
#     id: int = Field(alias="identifier")
# and for the Config Class -> must have :
# "allow_population_by_field_name = True" # This just for the usage of alias.
# also, for the response must have a Config class
# with orm_mode = True

