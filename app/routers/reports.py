from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db
from datetime import date

router = APIRouter(
    prefix="/reports",
    tags=['Reports']
)

# • Current active flight
# • Percentage of booking in every flight on a given date
# • Payments that have been confirmed and complete
# • Waitlisted passengers in each class given a flight number
# • Average load factor (percentage of seats occupied divided by total seats) for all planes on a given date
# • Ticket cancelled

@router.get("/", status_code=HTTP_200_OK)
def get_routes(current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        route = {
            "Current active flight":"/flights",
            "Percentage of booking in every flight on a given date":"/flights/date",
            "Payments that have been confirmed and complete":"/payments",
            "Waitlisted passengers in each class given a flight number":"/waitlists",
            "Average load factor (percentage of seats occupied divided by total seats) for all planes on a given date":"/loads/date",
            "Ticket cancelled":"/tickets",
        }
        
        return route
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/flights", status_code=HTTP_200_OK, response_model=List[schemas.FlightRES])
def get_active_flights(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        state = db.query(models.State).filter(models.State.state == "Active").first()
        if not state:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no state with active registed.")
        
        flight = db.query(models.Flight).filter(models.Flight.state_id == state.id).all()
        if not flight:
            raise HTTPException(status_code=HTTP_202_ACCEPTED, detail=f"There is no active flight.")
        
        
        return flight
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/flights/{date}", status_code=HTTP_200_OK)
def get_percantage(date: date, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        lDict = list() # list of dictionaries for the return.
        
        flights = db.query(models.Flight).filter(models.Flight.tdate == date).all()
        if not flights:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no flight on {date}.")
        
        state = db.query(models.State).filter(models.State.state == "Confirmed").first()
        if not state:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no state with confirmed registed.")
        
        for i in flights:
            all = 0
            confiremed = 0
            
            all_ticket = db.query(models.Ticket).filter(models.Ticket.flight_id == i.id)
            aticket = all_ticket.all()
            if not aticket:
                lDict.append({"flight_id": f"{i.id}",
                        "error":f"there is no ticket with flight id {i.id}"})
                continue
            else:
                all = len(aticket)
            
            confiremed_ticket = db.query(models.Ticket).filter(models.Ticket.flight_id == i.id).filter(models.Ticket.state_id == 7)
            cticket = confiremed_ticket.all()
            if not cticket:
                confiremed_ticket = -1
            else:
                confiremed = len(cticket)
            
            
            per = str(((confiremed) / (all)) * 100) + "%"
            
            lDict.append({
                "flight_id": f"{i.id}",
                "percantage": per,
            })
        
        
        return lDict
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/payments", status_code=HTTP_200_OK)
def get_payment(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        state = db.query(models.State).filter(models.State.state == "Confirmed").first()
        if not state:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no state with Confirmed registed.")
        
        order = db.query(models.Order).filter(models.Order.state_id == state.id).all()
        if not order:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no order confirmed registed.")
        
        
        return order
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/waitlists/{id}", status_code=HTTP_200_OK, response_model=List[schemas.WaitListRES])
def get_waitlist(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        waitlist = db.query(models.WaitList).filter(models.WaitList.flight_id == id).all()
        if not waitlist:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no waitlist registed.")
        
        
        return waitlist
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/loads/{date}", status_code=HTTP_200_OK)
def get_order(date: date, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        lDict = list()
        
        flights = db.query(models.Flight).filter(models.Flight.tdate == date).all()
        if not flights:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no flight on {date}.")
        
        state = db.query(models.State).filter(models.State.state == "Confirmed").first()
        if not state:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no state with Confirmed registed.")
        
        temp = len(flights)+0
        for i in flights:
            
            all = 0
            confiremed = 0
            
            all_ticket = db.query(models.Ticket).filter(models.Ticket.flight_id == i.id)
            aticket = all_ticket.all()
            if not aticket:
                continue
            else:
                all = len(aticket)
            
            confiremed_ticket = db.query(models.Ticket).filter(models.Ticket.flight_id == i.id).filter(models.Ticket.state_id == 7)
            cticket = confiremed_ticket.all()
            if not cticket:
                confiremed_ticket = -1
            else:
                confiremed = len(cticket)
            
            
            per = (((confiremed) / (all)) * 100)
            
            
            lDict.append(per)
        
        avg = sum(lDict)/ temp
        tt = str(avg) + "%"
        return {"Average load factor" : tt}
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/tickets", status_code=HTTP_200_OK, response_model=List[schemas.TicketRES])
def get_ticket(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        state = db.query(models.State).filter(models.State.state == "Canceled").first()
        if not state:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no state with Canceled registed.")
        
        ticket = db.query(models.Ticket).filter(models.Ticket.state_id == state.id).all()
        if not ticket:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no canceled ticket registed.")
        
        
        return ticket
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
