from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db

#Done
router = APIRouter(
    prefix="/types",
    tags=['Types']
)

# Schemas:
    # TypeREQ -> Request Header/content
    # TypeRES -> Response model
# accessing DataBase db: Session = Depends(get_db)
# to verify you'r logedin current_user: int = Depends(oauth2.get_current_user)

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.TypeRES)
def create_type(type: schemas.TypeREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        type = models.Type(**type.dict())
        
        # does it exist?
        verify_type = db.query(models.Type).filter(models.Type.name == type.name).filter(models.Type.model == type.model).first()
        if verify_type:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is already {type.name}-{type.model} exists.")
        
        db.add(type)
        db.commit()
        db.refresh(type)
        return type
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/", status_code=HTTP_200_OK, response_model=List[schemas.TypeRES])
def get_type(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        type = db.query(models.Type).all()
        if not type:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no type registed.")
        
        
        return type
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.put("/{id}", status_code=HTTP_202_ACCEPTED, response_model=schemas.TypeRES)
def update_type(id: int, type: schemas.TypeUpdateREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        type_id = db.query(models.Type).filter(models.Type.id == id)
        tID = type_id.first()
        if not tID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Type with id {id} is not registed.")
        
        if tID.model == type.model and tID.name == type.name:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Type {tID.name}-{tID.model} already exists.")
        
        if type.model is None:
            type.model = tID.model
        if type.name is None:
            type.name = tID.name
        if type.engine is None:
            type.engine = tID.engine
        if type.max_speed is None:
            type.max_speed = tID.max_speed
        if type.number_engine is None:
            type.number_engine = tID.number_engine
        if type.configuration_seat_Business is None:
            type.configuration_seat_Business = tID.configuration_seat_Business
        if type.configuration_seat_Economy is None:
            type.configuration_seat_Economy = tID.configuration_seat_Economy
        if type.configuration_seat_FirstClass is None:
            type.configuration_seat_FirstClass = tID.configuration_seat_FirstClass
        if type.configuration_seat_PremiumEconomy is None:
            type.configuration_seat_PremiumEconomy = tID.configuration_seat_PremiumEconomy
        if type.number_seat_Economy is None:
            type.number_seat_Economy = tID.number_seat_Economy
        if type.number_seat_Business is None:
            type.number_seat_Business = tID.number_seat_Business
        if type.number_seat_FirstClass is None:
            type.number_seat_FirstClass = tID.number_seat_FirstClass
        if type.number_seat_PremiumEconomy is None:
            type.number_seat_PremiumEconomy = tID.number_seat_PremiumEconomy
        
        type_id.update(type.dict(), synchronize_session=False)
        db.commit()
        
        return type_id.first()
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_type(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        type_id = db.query(models.Type).filter(models.Type.id == id)
        tID = type_id.first()
        if not tID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Type with id {id} is not registed.")
        
        
        type_id.delete(synchronize_session=False)
        db.commit()
        return
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

