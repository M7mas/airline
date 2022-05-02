from statistics import mode
from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import get_db


router = APIRouter(
    prefix="/users",
    tags=['Users']
)



@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.CreateUserPOST)
def create_user(user: schemas.CreateUserREQ, db: Session = Depends(get_db)):
    
    hashed_password = utils.Hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    
    # checking if the user already exist:
    user = db.query(models.User).filter(models.User.email == user.email).first()
    if user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"User with email: {user.email} already exist.")
    
    # creating a new user
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.get("/{id}", status_code=HTTP_200_OK, response_model=schemas.CreateUserPOST)
def get_user(id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist.")
    return user


@router.get("/", status_code=HTTP_200_OK, response_model=List[schemas.CreateUserPOST])
def get_users(db: Session = Depends(get_db)):
    
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"There is no Users.")
    return users

