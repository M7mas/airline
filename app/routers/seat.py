from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db

#Done
router = APIRouter(
    prefix="/seats",
    tags=['Seats']
)
# Schemas:
    # SeatREQ -> Request Header/content
    # SeatRES -> Response model
# accessing DataBase db: Session = Depends(get_db)
# to verify you'r logedin current_user: int = Depends(oauth2.get_current_user)

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.SeatRES)
def create_seat(seat: schemas.SeatREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        seat = models.Seat(**seat.dict())
        
        # does it exist?
        verify_seat = db.query(models.Seat).filter(models.Seat.rows == seat.rows).filter(models.Seat.cols == seat.cols).first()
        if verify_seat:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is already a seat {seat.rows}-{seat.cols} exists.")
        
        db.add(seat)
        db.commit()
        db.refresh(seat)
        return seat
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/", status_code=HTTP_200_OK, response_model=List[schemas.SeatRES])
def get_seat(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        
        seat = db.query(models.Seat).all()
        if not seat:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no seat registed.")
        
        
        return seat
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.put("/{id}", status_code=HTTP_202_ACCEPTED, response_model=schemas.SeatRES)
def update_seat(id: int, seat: schemas.SeatUpdateREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        seat.id = id        
        # does it exist?
        seat_id = db.query(models.Seat).filter(models.Seat.id == id)
        sID = seat_id.first()
        if not sID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Seat with id {id} is not registed.")
        
        if seat.cols is None:
            seat.cols = sID.cols
        if seat.rows is None:
            seat.rows = sID.rows
        
        seat_id.update(seat.dict(), synchronize_session=False)
        db.commit()
        return seat_id.first()
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_seat(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        seat_id = db.query(models.Seat).filter(models.Seat.id == id)
        sID = seat_id.first()
        if not sID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Seat with id {id} is not registed.")
        
        
        seat_id.delete(synchronize_session=False)
        db.commit()
        return
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
