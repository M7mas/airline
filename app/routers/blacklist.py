from tkinter.messagebox import NO
from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db

# Done
router = APIRouter(
    prefix="/blacklists",
    tags=['BlackLists']
)

# Schemas:
    # BlackListREQ -> Request Header/content
    # BlackListRES -> Response model
# accessing DataBase db: Session = Depends(get_db)
# to verify you'r logedin current_user: int = Depends(oauth2.get_current_user)

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.BlackListRES)
def create_blacklist(blacklist: schemas.BlackListREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        blacklist = models.Blacklist(**blacklist.dict())

        # does it exist?
        verify_existing = db.query(models.User).filter(models.User.id == blacklist.user_id).first()
        if not verify_existing:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is not user with id {blacklist.user_id}.")

        verify_existing_blacklist = db.query(models.Blacklist).filter(models.Blacklist.user_id == blacklist.user_id).first()
        if verify_existing_blacklist:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Already user with id {blacklist.user_id} is blacklisted.")
        
        db.add(blacklist)
        db.commit()
        db.refresh(blacklist)
        return blacklist
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/", status_code=HTTP_200_OK, response_model=List[schemas.BlackListRES])
def get_blacklist(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        blacklist = db.query(models.Blacklist).all()
        if not blacklist:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no users blacklisted.")
        
        
        return blacklist
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.put("/{id}", status_code=HTTP_202_ACCEPTED)
def update_blacklist(id: int, blacklist: schemas.BlackListUpdateREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        
        verify_existing_blacklist = db.query(models.Blacklist).filter(models.Blacklist.user_id == id)
        bl = verify_existing_blacklist.first()
        if not bl:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"User with id {id} is not blacklisted.")
        
        blacklist.user_id = id
        
        if blacklist.title == None:
            blacklist.title = bl.title
        if blacklist.description == None:
            blacklist.description = bl.description
        
        
        verify_existing_blacklist.update(blacklist.dict(), synchronize_session=False)
        db.commit()
        
        return verify_existing_blacklist.first()
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def update_blacklist(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        
        verify_existing_blacklist = db.query(models.Blacklist).filter(models.Blacklist.user_id == id)
        bl = verify_existing_blacklist.first()
        if not bl:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"User with id {id} is not blacklisted.")
        
        
        verify_existing_blacklist.delete(synchronize_session=False)
        db.commit()
        
        return
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
