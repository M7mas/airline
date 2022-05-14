from datetime import timedelta, date
from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db


router = APIRouter(
    prefix="/orders",
    tags=['Orders']
)

# Schemas:
    # OrderREQ -> Request Header/content
    # OrderRES -> Response model
# accessing DataBase db: Session = Depends(get_db)
# to verify you'r logedin current_user: int = Depends(oauth2.get_current_user)

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.OrderRES)
def create_order(order: schemas.OrderREQ, ticket: Optional[schemas.TicketUpdateState], db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = True
    
    if flag:
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
        
        if not ((verify_ticket.state_id == class_empty.id) or (verify_ticket.class_id == class_cancenled.id)):
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
        
        return order
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/", status_code=HTTP_200_OK, response_model=List[schemas.OrderRES])
def get_order(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        
        order = db.query(models.Order).all()
        if not order:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no order registed.")
        
        
        return order
    else:
        order = db.query(models.Order).filter(models.Order.user_id == current_user.id).all()
        if not order:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no order registed.")
        return order

@router.get("/{id}", status_code=HTTP_200_OK, response_model=List[schemas.OrderRES])
def get_order(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        
        order = db.query(models.Order).filter(models.Order.id == id).first()
        if not order:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no order registed.")
        
        
        return order
    else:
        order = db.query(models.Order).filter(models.Order.user_id == current_user.id).filter(models.Order.id == id).first()
        if not order:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no order registed.")
        return order



@router.put("/{id}", status_code=HTTP_202_ACCEPTED, response_model=schemas.OrderRES)
def update_order(id: int, order: schemas.OrderUpdateREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        # does it exist?
        order_id = db.query(models.Order).filter(models.Order.id == id)
        oID = order_id.first()
        if not oID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Order with id {id} is not registed.")
        
        if order.fname is None:
            order.fname = oID.fname
        
        if order.mname is None:
            order.mname = oID.mname
        
        if order.lname is None:
            order.lname = oID.lname
        
        
        order_id.update(order.dict(), synchronize_session=False)
        db.commit()
        return order_id.first()
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_order(id: int, delete: Optional[schemas.OrderDeleteREQ], db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        order_id = db.query(models.Order).filter(models.Order.id == id)
        oID = order_id.first()
        if not oID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Order with id {id} is not registed.")
        
        
        order_id.delete(synchronize_session=False)
        db.commit()
        
        class_cancenled = db.query(models.State).filter(models.State.state == "Canceled").first()
        
        if not class_cancenled:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"The class with Cancel does not exists.")
        
        
        ticket_id = db.query(models.Ticket).filter(models.Ticket.id == id).filter(models.Ticket.state_id == class_cancenled.id)
        tID = ticket_id.first()
        if not oID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Ticket with id {tID.id} is not registed.")
        
        delete.class_id = 4
        ticket_id.update(delete.dict(), synchronize_session=False)
        db.commit()
        
        return
    else:
        
        order_id = db.query(models.Order).filter(models.Order.id == id).filter(models.Order.user_id == cu.id)
        oID = order_id.first()
        if not oID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Order with id {id} is not registed.")
        
        
        order_id.delete(synchronize_session=False)
        db.commit()
        
        class_cancenled = db.query(models.State).filter(models.State.state == "Canceled").first()
        
        if not class_cancenled:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"The class with Cancel does not exists.")
        
        
        ticket_id = db.query(models.Ticket).filter(models.Ticket.id == id).filter(models.Ticket.state_id == class_cancenled.id)
        tID = ticket_id.first()
        if not oID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Ticket with id {tID.id} is not registed.")
        
        delete.class_id = 4
        ticket_id.update(delete.dict(), synchronize_session=False)
        db.commit()
        
        return 








