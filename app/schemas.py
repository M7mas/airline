from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# This class responsible for handling ->/<- the API.
# request to the API
# response from the API
# responses must have Config class

######################################################## --- Else-Models --- ##############################################
class UserPublicInfo(BaseModel):
    email: EmailStr
    
    class Config: # This only for the response
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[str] = None




######################################################## --- Request --- ##############################################
class CreateUserREQ(BaseModel):
    email: EmailStr 
    password: str
    phone_number: Optional[str] = None

class UserLoginREQ(BaseModel):
    email: EmailStr 
    password: str

class TokenREQ(BaseModel):
    access_token: str
    token_type: str



class PostCreateREQ(BaseModel):
    title: str 
    content: str 
    private: bool = False


######################################################## --- Response --- ##############################################
class CreateUserPOST(BaseModel):
    id: int 
    email: EmailStr 
    # password: str 
    created_at: datetime
    
    class Config: # This only for the response
        orm_mode = True



class Testing(BaseModel):
    id: int 
    title: str
    content: str 
    private: bool 
    created_at: datetime
    owner_id: int = Field(alias="user_id")
    owner: UserPublicInfo = Field(alias="user")
    
    class Config: # This only for the response
        orm_mode = True
        allow_population_by_field_name = True # This just for the usage of alias.


# in order to use alias ->
# after the type : "= Field(alias="The_Name")"
# exp.:
#     id: int = Field(alias="identifier")
# and for the Config Class -> must have :
# "allow_population_by_field_name = True" # This just for the usage of alias.

