from datetime import date, timedelta
from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db


router = APIRouter(
    prefix="/waitlists",
    tags=['WaitLists']
)

# Schemas:
    # WaitListREQ -> Request Header/content
    # WaitListRES -> Response model
# accessing DataBase db: Session = Depends(get_db)
# to verify you'r logedin current_user: int = Depends(oauth2.get_current_user)

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.WaitListRES)
def create_waitlist(waitlist: schemas.WaitListREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = True
    
    if flag:
        waitlist = models.WaitList(**waitlist.dict())
        
        # does it exist?
        verify_flight = db.query(models.Flight).filter(models.Flight.id == waitlist.flight_id).first()
        
        if not verify_flight:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no flight with id {waitlist.flight_id} exists.")
        
        plane_id = verify_flight.plane_id
        verify_plane = db.query(models.Plane).filter(models.Plane.id == plane_id).first()
        if not verify_plane:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no plane with id {plane_id} exists.")
        
        type_id = verify_plane.type_id
        verify_type = db.query(models.Type).filter(models.Type.id == type_id).first()
        if not verify_type:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no type with id {type_id} exists.")
        
        verify_user = db.query(models.User).filter(models.User.id == waitlist.user_id).first()
        if not verify_user:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no user with id {waitlist.user_id} exists.")
        
        verify_class = db.query(models.TClass).filter(models.TClass.id == waitlist.class_id).first()
        if not verify_class:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no class with id {waitlist.class_id} exists.")
        
        verify_waitlist = db.query(models.WaitList).filter(models.WaitList.user_id == waitlist.user_id).filter(models.WaitList.flight_id == waitlist.flight_id).first()
        if verify_waitlist:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is already a waitlist with user: {waitlist.user_id}, flight: {waitlist.flight_id} exists.")
        
        # This checking is for 10 eco; 3 others.
        
        if waitlist.class_id == 4:
            
            eco = db.query(models.WaitList).filter(models.WaitList.flight_id == waitlist.flight_id).filter(models.WaitList.class_id == 4).all()
            
            if len(eco) >= 10:
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There are already 10 registered for this flight {waitlist.flight_id}.")
            else:
                db.add(waitlist)
                db.commit()
                db.refresh(waitlist)
                return waitlist
            
        elif waitlist.class_id == 2:
            
            bus = db.query(models.WaitList).filter(models.WaitList.flight_id == waitlist.flight_id).filter(models.WaitList.class_id == 2).all()
            if len(bus) >= 3:
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There are already 3 registered for this flight {waitlist.flight_id}.")
            else:
                db.add(waitlist)
                db.commit()
                db.refresh(waitlist)
                return waitlist
            
        elif waitlist.class_id == 1:
            
            first = db.query(models.WaitList).filter(models.WaitList.flight_id == waitlist.flight_id).filter(models.WaitList.class_id == 1).all()
            if len(first) >= 3:
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There are already 3 registered for this flight {waitlist.flight_id}.")
            else:
                db.add(waitlist)
                db.commit()
                db.refresh(waitlist)
                return waitlist
            
        elif waitlist.class_id == 3:
            
            premEco = db.query(models.WaitList).filter(models.WaitList.flight_id == waitlist.flight_id).filter(models.WaitList.class_id == 3).all()
            if len(premEco) >= 3:
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There are already 3 registered for this flight {waitlist.flight_id}.")
            else:
                db.add(waitlist)
                db.commit()
                db.refresh(waitlist)
                return waitlist
            
        else:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=f"There is no class other than First, business, premium economy and economy.")
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/", status_code=HTTP_200_OK, response_model=List[schemas.WaitListRES])
def get_waitlist(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        
        waitlist = db.query(models.WaitList).all()
        if not waitlist:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no waitlist registed.")
        
        
        return waitlist
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.put("/{id}", status_code=HTTP_202_ACCEPTED, response_model=schemas.WaitListRES)
def update_waitlist(id: int, waitlist: schemas.WaitListUpdateREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        # does it exist?
        waitlist_id = db.query(models.WaitList).filter(models.WaitList.id == id)
        wID = waitlist_id.first()
        if not wID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"waitlist with id {id} is not registed.")
        
        if waitlist.class_id is None:
            waitlist.class_id = wID.class_id
        if waitlist.flight_id is None:
            waitlist.flight_id = wID.flight_id
        if waitlist.user_id is None:
            waitlist.user_id = wID.user_id
        
        waitlist_id.update(waitlist.dict(), synchronize_session=False)
        db.commit()
        return waitlist_id.first()
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_waitlist(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        waitlist_id = db.query(models.WaitList).filter(models.WaitList.id == id)
        wID = waitlist_id.first()
        if not wID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"waitlist with id {id} is not registed.")
        
        
        waitlist_id.delete(synchronize_session=False)
        db.commit()
        return
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.put("/promote/{id}", status_code=HTTP_202_ACCEPTED, response_model=schemas.OrderRES)
def promote(id: int, order: schemas.OrderREQ, ticket: Optional[schemas.TicketUpdateState], db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        # does it exist?
        order = models.Order(**order.dict())
        
        # does it exist?
        # need to verify:
        
        
        verify_ticket = db.query(models.Ticket).filter(models.Ticket.id == order.ticket_id).first()
        if not verify_ticket:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no Ticket with id {order.ticket_id} exists.")
        
        verify_card = db.query(models.Card).filter(models.Card.id == order.card_id).filter(models.Card.user_id == current_user.id).first()
        if not verify_card:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no Card with user id {current_user.id} exists.")
        
        
        order.user_id = current_user.id
        order.flight_id = verify_ticket.flight_id
        verify_order = db.query(models.Order).filter(models.Order.user_id == order.user_id).filter(models.Order.flight_id == order.flight_id).all()
        ser = len(verify_order)
        
        if ser == 10:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"You can't order more than 10 ticket with the same flights.")
        order.state_id = 1
        order.serial = ser
        expdate = date.today()
        order.expiredate = expdate + timedelta(days=90)
        
        verify_ticket = db.query(models.Ticket).filter(models.Ticket.id == order.ticket_id).first() # is empty
        class_empty = db.query(models.State).filter(models.State.state == "Empty").first()
        class_cancenled = db.query(models.State).filter(models.State.state == "Canceled").first()
        
        if not ((verify_ticket.state_id == class_empty.id) or (verify_ticket.state_id == class_cancenled.id)):
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"The Seat is reserved.")
        
        
        db.add(order)
        db.commit()
        db.refresh(order)
        
        ticket.state_id = 7
        ticket_id = db.query(models.Ticket).filter(models.Ticket.id == order.ticket_id)
        tID = ticket_id.first()
        if not tID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Ticket with id {tID.id} is not registed.")
        
        ticket_id.update(ticket.dict(), synchronize_session=False)
        db.commit()
        
        waitlist_id = db.query(models.WaitList).filter(models.WaitList.id == id)
        wID = waitlist_id.first()
        if not wID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"waitlist with id {id} is not registed.")
        
        
        waitlist_id.delete(synchronize_session=False)
        db.commit()
        
        return order
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)