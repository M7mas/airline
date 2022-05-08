from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db

# Done
router = APIRouter(
    prefix="/states",
    tags=['States']
)



# Schemas:
    # StateREQ -> Request Header/content
    # StateRES -> Response model
# accessing DataBase db: Session = Depends(get_db)
# to verify you'r logedin current_user: int = Depends(oauth2.get_current_user)

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.StateRES)
def create_state(state: schemas.StateREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        state = models.State(**state.dict())
        
        # does it exist?
        verify_state = db.query(models.State).filter(models.State.state == state.state).first()
        if verify_state:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is already state {state.state} exists.")
        
        db.add(state)
        db.commit()
        db.refresh(state)
        return state
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/", status_code=HTTP_200_OK, response_model=List[schemas.StateRES])
def get_state(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        
        state = db.query(models.State).all()
        if not state:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no state registed.")
        
        
        return state
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.put("/{id}", status_code=HTTP_202_ACCEPTED, response_model=schemas.StateRES)
def update_state(id: int, state: schemas.StateREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        state_id = db.query(models.State).filter(models.State.id == id)
        sID = state_id.first()
        if not sID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"State with id {id} is not registed.")
        
        if sID.state == state.state:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"State {sID.state} already exists.")
        
        
        state_id.update(state.dict(), synchronize_session=False)
        db.commit()
        
        return state_id.first()
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_state(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        state_id = db.query(models.State).filter(models.State.id == id)
        sID = state_id.first()
        if not sID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"State with id {id} is not registed.")
        
        
        state_id.delete(synchronize_session=False)
        db.commit()
        return
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

