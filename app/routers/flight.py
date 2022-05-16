from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db

#Done
router = APIRouter(
    prefix="/flights",
    tags=['Flights']
)

# Schemas:
    # FlightREQ -> Request Header/content
    # FlightRES -> Response model
# accessing DataBase db: Session = Depends(get_db)
# to verify you'r logedin current_user: int = Depends(oauth2.get_current_user)


@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.FlightRES)
def create_flight(flight: schemas.FlightREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        flight = models.Flight(**flight.dict())
        
        # dep:
            # plane_id
            # state_id
        plane_id = flight.plane_id
        state_id = flight.state_id
        
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
        
        db.add(flight)
        db.commit()
        db.refresh(flight)
        return flight
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

# Change it so anyone can see the current flight, no need for prior login
# removed "current_user: int = Depends(oauth2.get_current_user)"
# ^ just to verify the token.
@router.get("/", status_code=HTTP_200_OK, response_model=List[schemas.FlightRES])
def get_flight(db: Session = Depends(get_db), uFrom: Optional[str] = "", uTo: Optional[str] = ""):
    
    flag = True
    
    if flag:
        
        flight = db.query(models.Flight).filter(models.Flight.source_city.contains(uFrom)).filter(models.Flight.source_city.contains(uTo)).all()
        if not flight:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no flight registed.")
        
        
        return flight
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/{id}", status_code=HTTP_200_OK, response_model=List[schemas.FlightRES])
def get_flight(id: int, db: Session = Depends(get_db)):
    
    flight = db.query(models.Flight).filter(models.Flight.id == id).first()
    if not flight:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no flight with id {id} registed.")
    
    return flight

@router.put("/{id}", status_code=HTTP_202_ACCEPTED, response_model=schemas.FlightRES)
def update_flight(id: int, flight: schemas.FlightUpdateREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        
        flight_id = db.query(models.Flight).filter(models.Flight.id == id)
        fID = flight_id.first()
        if not fID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Flight with id {id} is not registed.")
        
        
        if flight.source_city is None:
            flight.source_city = fID.source_city
        if flight.destination_city is None:
            flight.destination_city = fID.destination_city
        if flight.date is None:
            flight.date = fID.date
        if flight.state_id is None:
            flight.state_id = fID.state_id
        if flight.plane_id is None:
            flight.plane_id = fID.plane_id
        
        verify_fine = db.query(models.State).filter(models.State.id == flight.state_id).first()
        temp = verify_fine.state
        if temp == "Canceled" or temp == "Missed":
            tempo_dict = {"flight_id":id, "amount":"1500", "state_id":flight.state_id}
            tempo = models.Fine(**tempo_dict)
            db.add(tempo)
            db.commit()
            db.refresh(tempo)
        
        
        flight_id.update(flight.dict(), synchronize_session=False)
        db.commit()
        
        return flight_id.first()
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_flight(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        flight_id = db.query(models.Flight).filter(models.Flight.id == id)
        fID = flight_id.first()
        if not fID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Flight with id {id} is not registed.")
        
        
        flight_id.delete(synchronize_session=False)
        db.commit()
        return
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

