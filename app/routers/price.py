from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db


router = APIRouter(
    prefix="/prices",
    tags=['Prices']
)
# Schemas:
    # PriceREQ -> Request Header/content
    # PriceRES -> Response model
# accessing DataBase db: Session = Depends(get_db)
# to verify you'r logedin current_user: int = Depends(oauth2.get_current_user)

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.PriceRES)
def create_price(price: schemas.PriceREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        price = models.Price(**price.dict())
        
        # does it exist?
        verify_price = db.query(models.Price).filter(models.Price.price == price.price).first()
        if verify_price:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is already a price with {price.price} exists.")
        
        db.add(price)
        db.commit()
        db.refresh(price)
        return price
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/", status_code=HTTP_200_OK, response_model=List[schemas.PriceRES])
def get_price(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        
        price = db.query(models.Price).all()
        if not price:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no price registed.")
        
        
        return price
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.put("/{id}", status_code=HTTP_202_ACCEPTED, response_model=schemas.PriceRES)
def update_price(id: int, price: schemas.PriceREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        # does it exist?
        price_id = db.query(models.Price).filter(models.Price.id == id)
        pID = price_id.first()
        if not pID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Price with id {id} is not registed.")
        
        
        price_id.update(price.dict(), synchronize_session=False)
        db.commit()
        return price_id.first()
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_price(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        price_id = db.query(models.Price).filter(models.Price.id == id)
        pID = price_id.first()
        if not pID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Price with id {id} is not registed.")
        
        
        price_id.delete(synchronize_session=False)
        db.commit()
        return
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
