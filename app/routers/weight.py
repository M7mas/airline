from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db

#Done
router = APIRouter(
    prefix="/weights",
    tags=['Weights']
)

# Schemas:
    # WeightREQ -> Request Header/content
    # WeightRES -> Response model
# accessing DataBase db: Session = Depends(get_db)
# to verify you'r logedin current_user: int = Depends(oauth2.get_current_user)

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.WeightRES)
def create_weight(weight: schemas.WeightREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        weight = models.Weight(**weight.dict())
        
        # does it exist?
        verify_weight = db.query(models.Weight).filter(models.Weight.weight == weight.weight).first()
        if verify_weight:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is already a weight {weight.weight} exists.")
        
        db.add(weight)
        db.commit()
        db.refresh(weight)
        return weight
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/", status_code=HTTP_200_OK, response_model=List[schemas.WeightRES])
def get_weight(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        
        weight = db.query(models.Weight).all()
        if not weight:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no seat registed.")
        
        
        return weight
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.put("/{id}", status_code=HTTP_202_ACCEPTED, response_model=schemas.WeightRES)
def update_weight(id: int, weight: schemas.WeightREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        # does it exist?
        weight_id = db.query(models.Weight).filter(models.Weight.id == id)
        wID = weight_id.first()
        if not wID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"weight with id {id} is not registed.")
        
        
        weight_id.update(weight.dict(), synchronize_session=False)
        db.commit()
        return weight_id.first()
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_weight(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        weight_id = db.query(models.Weight).filter(models.Weight.id == id)
        wID = weight_id.first()
        if not wID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"weight with id {id} is not registed.")
        
        
        weight_id.delete(synchronize_session=False)
        db.commit()
        return
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)









