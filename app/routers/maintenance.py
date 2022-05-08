from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db


router = APIRouter(
    prefix="/maintenance",
    tags=['Maintenace']
)



# Schemas:
    # MaintenanceREQ -> Request Header/content
    # MaintenanceRES -> Response model
# accessing DataBase db: Session = Depends(get_db)
# to verify you'r logedin current_user: int = Depends(oauth2.get_current_user)

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.MaintenanceRES)
def create_maintenance(maintenance: schemas.MaintenanceREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        maintenance = models.Maintenance(**maintenance.dict())
        
        # does it exist?
        plane_id = maintenance.plane_id
        
        verify_plane = db.query(models.Plane).filter(models.Plane.id == plane_id).first()
        if not verify_plane:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no plane with id {plane_id} exists.")
        
        type_id = verify_plane.type_id
        verify_type = db.query(models.Type).filter(models.Type.id == type_id).first()
        if not verify_type:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no type with id {type_id} exists.")
        
        db.add(maintenance)
        db.commit()
        db.refresh(maintenance)
        return maintenance
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.get("/", status_code=HTTP_200_OK, response_model=List[schemas.MaintenanceRES])
def get_maintenance(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        
        maintenance = db.query(models.Maintenance).all()
        if not maintenance:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no maintenance registed.")
        
        
        return maintenance
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.put("/{id}", status_code=HTTP_202_ACCEPTED, response_model=schemas.MaintenanceRES)
def update_maintenance(id: int, maintenance: schemas.MaintenanceUpdateREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        maintenance_id = db.query(models.Maintenance).filter(models.Maintenance.id == id)
        mID = maintenance_id.first()
        if not mID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"maintenance with id {id} is not registed.")
        
        if maintenance.last_date is None:
            maintenance.last_date = mID.last_date
        if maintenance.next_date is None:
            maintenance.next_date = mID.next_date
        if maintenance.plane_id is None:
            maintenance.plane_id = mID.plane_id
        
        maintenance_id.update(maintenance.dict(), synchronize_session=False)
        db.commit()
        
        return maintenance_id.first()
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_maintenance(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    cu = current_user.role
    if cu == "admin" or cu == "root":
        flag = True
    
    if flag:
        
        # does it exist?
        maintenance_id = db.query(models.Maintenance).filter(models.Maintenance.id == id)
        mID = maintenance_id.first()
        if not mID:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"maintenance with id {id} is not registed.")
        
        
        maintenance_id.delete(synchronize_session=False)
        db.commit()
        return
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

