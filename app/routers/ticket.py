from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db



#Done
router = APIRouter(
    prefix="/tickets",
    tags=['Tickets']
)

# Schemas:
    # TicketREQ -> Request Header/content
    # TicketRES -> Response model
# accessing DataBase db: Session = Depends(get_db)
# to verify you'r logedin current_user: int = Depends(oauth2.get_current_user)

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.TicketRES)
def create_ticket(tickets: schemas.TicketREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        tickets = models.Ticket(**tickets.dict())
        
        # does it exist?
        # need to verify:
                # weight_id: int
                # state_id: int
                # seat_id: int
                # price_id: int
        
        
        verify_flight = db.query(models.Flight).filter(models.Flight.id == tickets.flight_id).first()
        if not verify_flight:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no flight with id {tickets.flight_id} exists.")
        
        plane_id = verify_flight.plane_id
        verify_plane = db.query(models.Plane).filter(models.Plane.id == plane_id).first()
        if not verify_plane:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no plane with id {plane_id} exists.")
        
        type_id = verify_plane.type_id
        verify_type = db.query(models.Type).filter(models.Type.id == type_id).first()
        if not verify_type:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no type with id {type_id} exists.")
        
        verify_class = db.query(models.TClass).filter(models.TClass.id == tickets.class_id).first()
        if not verify_class:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no class with id {tickets.class_id} exists.")
        
        weight_id =  tickets.weight_id
        verify_weight = db.query(models.Weight).filter(models.Weight.id == weight_id).first()
        if not verify_weight:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no weight with id {weight_id} exists.")
        
        state_id = tickets.state_id
        verify_state = db.query(models.State).filter(models.State.id == state_id).first()
        if not verify_state:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no state with id {state_id} exists.")
        
        seat_id = tickets.seat_id
        verify_seat = db.query(models.Seat).filter(models.Seat.id == seat_id).first()
        if not verify_seat:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no seat with id {verify_seat} exists.")
        
        price_id = tickets.price_id
        verify_price = db.query(models.Price).filter(models.Price.id == price_id).first()
        if not verify_price:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no price with id {price_id} exists.")
        
        verify_ticket = db.query(models.Ticket).filter(models.Ticket.flight_id == tickets.flight_id).filter(models.Ticket.seat_id == seat_id).first()
        if verify_ticket:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is already ticket with flight-id {tickets.flight_id}, seat-id {seat_id} exists.")
        
        db.add(tickets)
        db.commit()
        db.refresh(tickets)
        return tickets
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/", status_code=HTTP_200_OK, response_model=List[schemas.TicketRES])
def get_ticket(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        
        ticket = db.query(models.Ticket).all()
        if not ticket:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no ticket registed.")
        
        
        return ticket
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.put("/{id}", status_code=HTTP_202_ACCEPTED, response_model=schemas.TicketRES)
def update_ticket(id: int, tickets: schemas.TicketUpdateREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        # does it exist?
        ticket_id = db.query(models.Ticket).filter(models.Ticket.id == id)
        tID = ticket_id.first()
        if not tID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Ticket with id {id} is not registed.")
        
        if tickets.time is None:
            tickets.time = tID.time
        if tickets.weight_id is None:
            tickets.weight_id = tID.weight_id
        if tickets.state_id is None:
            tickets.state_id = tID.state_id
        if tickets.class_id is None:
            tickets.class_id = tID.class_id
        if tickets.price_id is None:
            tickets.price_id = tID.price_id
        
        
        ticket_id.update(tickets.dict(), synchronize_session=False)
        db.commit()
        return ticket_id.first()
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_ticket(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        ticket_id = db.query(models.Ticket).filter(models.Ticket.id == id)
        tID = ticket_id.first()
        if not tID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Ticket with id {id} is not registed.")
        
        
        ticket_id.delete(synchronize_session=False)
        db.commit()
        return
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)







