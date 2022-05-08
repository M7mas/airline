from pydoc import plain
from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db






#Done
router = APIRouter(
    prefix="/planes",
    tags=['Planes']
)
# Schemas:
    # PlaneREQ -> Request Header/content
    # PlaneRES -> Response model
# accessing DataBase db: Session = Depends(get_db)
# to verify you'r logedin current_user: int = Depends(oauth2.get_current_user)


@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.PlaneRES)
def create_plane(plane: schemas.PlaneREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        plane = models.Plane(**plane.dict())
        
        # does it exist?
        verify = db.query(models.Type).filter(models.Type.id == plane.type_id).first()
        if not verify:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no type with id {plane.type_id} exists.")
        
        db.add(plane)
        db.commit()
        db.refresh(plane)
        return plane
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/", status_code=HTTP_200_OK, response_model=List[schemas.PlaneRES])
def get_plane(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        
        plane = db.query(models.Plane).all()
        if not plane:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no plane registed.")
        
        
        return plane
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.put("/{id}", status_code=HTTP_202_ACCEPTED, response_model=schemas.PlaneRES)
def update_plane(id: int, plane: schemas.PlaneREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        verify = db.query(models.Type).filter(models.Type.id == plane.type_id).first()
        if not verify:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no type with id {plane.type_id} exists.")
        
        plane_id = db.query(models.Plane).filter(models.Plane.id == id)
        pID = plane_id.first()
        if not pID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Plane with id {id} is not registed.")
        
        
        plane_id.update(plane.dict(), synchronize_session=False)
        db.commit()
        
        return plane_id.first()
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_plane(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        plane_id = db.query(models.Plane).filter(models.Plane.id == id)
        pID = plane_id.first()
        if not pID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Plane with id {id} is not registed.")
        
        
        plane_id.delete(synchronize_session=False)
        db.commit()
        return
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)