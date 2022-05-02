from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db


router = APIRouter(
    prefix="/sql",
    tags=['Testing']
)
# current_user: int = Depends(oauth2.get_current_user)
# is just to force a user to be logedin, and must have a token

@router.get("/", status_code=HTTP_200_OK, response_model=List[schemas.Testing])
def test(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    temp = db.query(models.Temp).join(models.User, models.User.id == models.Temp.owner_id).all()
    if not temp:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"not found.")
    return temp

@router.get("/{id}", status_code=HTTP_200_OK, response_model=schemas.Testing)
def tem(id: int, db: Session = Depends(get_db)):
    
    temp = db.query(models.Temp).join(models.User, models.Temp.owner_id == models.User.id).filter(models.Temp.id == id).first()
    if not temp:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"not found.")
    return temp


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Testing)
def create_posts(post:schemas.PostCreateREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    if current_user is None:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=f"You need to be logedin before creating a post.")
    
    new_post = models.Temp(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


