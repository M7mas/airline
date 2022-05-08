from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db

# Done
router = APIRouter(
    prefix="/classes",
    tags=['Classes']
)


# Schemas:
    # ClassREQ -> Request Header/content
    # ClassRES -> Response model
# accessing DataBase db: Session = Depends(get_db)
# to verify you'r logedin current_user: int = Depends(oauth2.get_current_user)

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.ClassRES)
def create_class(classes: schemas.ClassREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        classes = models.TClass(**classes.dict())
        
        # does it exist?
        verify_class = db.query(models.TClass).filter(models.TClass.classes == classes.classes).first()
        if verify_class:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is already class {classes.classes} exists.")
        
        db.add(classes)
        db.commit()
        db.refresh(classes)
        return classes
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/", status_code=HTTP_200_OK, response_model=List[schemas.ClassRES])
def get_class(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        classes = db.query(models.TClass).all()
        if not classes:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no class registed.")
        
        
        return classes
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.put("/{id}", status_code=HTTP_202_ACCEPTED, response_model=schemas.ClassRES)
def update_class(id: int, classes: schemas.ClassREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        class_id = db.query(models.TClass).filter(models.TClass.id == id)
        cID = class_id.first()
        if not cID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Class with id {id} is not registed.")
        
        if cID.classes == classes.classes:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Class {cID.classes} already exists.")
        
        
        class_id.update(classes.dict(), synchronize_session=False)
        db.commit()
        
        return class_id.first()
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_class(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        class_id = db.query(models.TClass).filter(models.TClass.id == id)
        cID = class_id.first()
        if not cID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Class with id {id} is not registed.")
        
        
        class_id.delete(synchronize_session=False)
        db.commit()
        return
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
