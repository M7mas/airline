from turtle import mode
from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db

#Done
router = APIRouter(
    prefix="/fines",
    tags=['Fines']
)


# Schemas:
    # FineREQ -> Request Header/content
    # FineRES -> Response model
# accessing DataBase db: Session = Depends(get_db)
# to verify you'r logedin current_user: int = Depends(oauth2.get_current_user)

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.FineRES)
def create_fine(fine: schemas.FineREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        fine = models.Fine(**fine.dict())
        
        # does it exist?
        flight_id = fine.flight_id
        verify_flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()
        if not verify_flight:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no flight with id {flight_id} exists.")
        flight = verify_flight
        plane_id = flight.plane_id
        state_id = fine.state_id
        
        verify_plane = db.query(models.Plane).filter(models.Plane.id == plane_id).first()
        if not verify_plane:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no plane with id {plane_id} exists.")
        
        type_id = verify_plane.type_id
        verify_type = db.query(models.Type).filter(models.Type.id == type_id).first()
        if not verify_type:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no type with id {type_id} exists.")
        
        verify_state = db.query(models.State).filter(models.State.id == state_id).first()
        if not verify_state:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no state with id {state_id} exists.")
        
        verify_fine = db.query(models.Fine).filter(models.Fine.flight_id == fine.flight_id).first()
        if verify_fine:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is already a fine with flight id {fine.flight_id} exists.")
        
        db.add(fine)
        db.commit()
        db.refresh(fine)
        return fine
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/", status_code=HTTP_200_OK, response_model=List[schemas.FineREQ])
def get_fine(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        fine = db.query(models.Fine).all()
        if not fine:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no class registed.")
        
        
        return fine
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.put("/{id}", status_code=HTTP_202_ACCEPTED, response_model=schemas.FineRES)
def update_fine(id: int, fine: schemas.FineUpdateREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        fine_id = db.query(models.Fine).filter(models.Fine.flight_id == id)
        fID = fine_id.first()
        if not fID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Fine with id {id} is not registed.")
        
        fine.flight_id = id
        if fine.amount is None:
            fine.amount = fID.amount
        if fine.state_id is None:
            fine.state_id = fID.state_id
        
        
        fine_id.update(fine.dict(), synchronize_session=False)
        db.commit()
        
        return fine_id.first()
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_fine(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        fine_id = db.query(models.Fine).filter(models.Fine.flight_id == id)
        fID = fine_id.first()
        if not fID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Fine with id {id} is not registed.")
        
        
        fine_id.delete(synchronize_session=False)
        db.commit()
        return
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

