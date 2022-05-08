from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db

# Done
router = APIRouter(
    prefix="/cards",
    tags=['Cards']
)

@router.get("/", status_code=HTTP_200_OK, response_model=List[schemas.CardsRES]) #get
def get_card(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    cards = db.query(models.Card).filter(models.Card.user_id == current_user.id).all()
    if not cards:
        raise HTTPException(HTTP_404_NOT_FOUND, detail=f"You don't have any card registered.")
    return cards

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.CardsRES) #create
def create_card(card: schemas.CardsREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    card.user_id = current_user.id
    new_card = models.Card(**card.dict())
    
    #checking if the card exist for this user
    verify_card = db.query(models.Card).filter(models.Card.user_id == current_user.id).filter(models.Card.number == card.number).first()
    if verify_card:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"This card already exist.")

    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    
    return new_card


@router.put("/{id}", status_code=HTTP_202_ACCEPTED, response_model=schemas.CardsRES) #update
def update_card(id:int, updated_card: schemas.CardUpdateREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    card_query = db.query(models.Card).filter(models.Card.user_id == current_user.id).filter(models.Card.id == id)
    card = card_query.first()
    
    if not card:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no card with id {id} exist.")
    
    updated_card.user_id = current_user.id
    card_query.update(updated_card.dict(), synchronize_session=False)
    db.commit()
    
    return card_query.first()


@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT) #delete
def delete_card(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    card_query = db.query(models.Card).filter(models.Card.user_id == current_user.id).filter(models.Card.id == id)
    card = card_query.first()
    
    if not card:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no card with id {id} exist.")
    
    card_query.delete(synchronize_session=False)
    db.commit()
    return 
