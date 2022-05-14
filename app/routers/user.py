from starlette.status import *
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas, utils
from app.database import get_db

# Done
router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.UserSignUpRES)
def create_user(user: schemas.UserSignUpREQ, db: Session = Depends(get_db)):
    
    hashed_password = utils.Hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    
    # checking if the user already exist:
    email = db.query(models.User).filter(models.User.email == user.email).first()
    if email:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"User with email: {user.email} already exist.")
    
    # creating a new user
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    #This to insert a passenger immediately after making a new user.
    custom_dict = {
                "user_id": new_user.id,
                "points":"0",
                }
    
    passenger = models.Passenger(**custom_dict)
    db.add(passenger)
    db.commit()
    db.refresh(passenger)
    return new_user


@router.get("/{id}", status_code=HTTP_200_OK, response_model=schemas.UserSignUpRES)
def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False

    if(current_user.role == "admin" or current_user.role == "root"):
        flag = True
    
    if (flag):
        
        try:
            user = db.query(models.User).filter(models.User.id == id).first()
        except:
            raise HTTPException(status_code=HTTP_424_FAILED_DEPENDENCY, detail=f"Try again")
            
        if not user:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist.")
        
        return user
    else:
        user_query = db.query(models.User).filter(models.User.id == id).filter(models.User.id == current_user.id).first()
        
        if not user_query:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no user with id {id} exist.")
        return user_query

@router.get("/", status_code=HTTP_200_OK, response_model=List[schemas.UserSignUpRES])
def get_users(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    
    if(current_user.role == "admin" or current_user.role == "root"):
        flag = True
    
    if (flag):
        try:
            users = db.query(models.User).all()
        except:
            raise HTTPException(status_code=HTTP_424_FAILED_DEPENDENCY, detail=f"Try again")

        if not users:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"There is no Users.")
        return users
    else:
        user_query = db.query(models.User).filter(models.User.id == id).filter(models.User.id == current_user.id).first()
        
        if not user_query:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no user with id {id} exist.")
        return user_query


@router.put("/{id}", status_code=HTTP_202_ACCEPTED, response_model=schemas.UserSignUpRES) #update
def update_user(id:int, updated_user: schemas.UserUpdateREQ, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    admin_flag = False
    hashed_password = utils.Hash(updated_user.password)
    updated_user.password = hashed_password
    
    if current_user.role == "admin" or current_user.role == "root":
        admin_flag = True
    
    if admin_flag:
        user_query = db.query(models.User).filter(models.User.id == id)
        user = user_query.first()
        
        if not user:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no user with id {id} exist.")
        
        if user.role == "root" and current_user.role != "root":
            return Response(status_code=HTTP_403_FORBIDDEN)
        
        user_query.update(updated_user.dict(), synchronize_session=False)
        db.commit()
        
        return user_query.first()
    
    else:
        user_query = db.query(models.User).filter(models.User.id == id).filter(models.User.id == current_user.id)
        user = user_query.first()
        
        if not user:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no user with id {id} exist.")
        
        user_query.update(updated_user.dict(), synchronize_session=False)
        db.commit()
        
        return user_query.first()


@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT) #delete
def delete_user(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    admin_flag = False
    
    
    if current_user.role == "admin" or current_user.role == "root":
        admin_flag = True
    
    if admin_flag:
        user_query = db.query(models.User).filter(models.User.id == id)
        user = user_query.first()
        
        if not user:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no user with id {id} exist.")
        
        if user.role == "root":
            return Response(status_code=HTTP_403_FORBIDDEN)
        
        user_query.delete(synchronize_session=False)
        db.commit()
        return 
    
    else:
        user_query = db.query(models.User).filter(models.User.id == id).filter(models.User.id == current_user.id)
        user = user_query.first()
        
        if not user:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no user with id {id} exist.")
        user_query.delete(synchronize_session=False)
        db.commit()
        return


@router.post("/admin/{id}", status_code=HTTP_202_ACCEPTED)
def make_admin(id: int, mAdmin: Optional[schemas.MakingAdminREQ],  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    flag = False
    
    if(current_user.role == "admin" or current_user.role == "root"):
        flag = True
    
    if (flag):
        
        
        try:
            user = db.query(models.User).filter(models.User.id == id)
            user_first = user.first()
            
            if not user:
                raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"There is no Users.")
            
            if user_first.role == "admin":
                raise HTTPException(status_code=HTTP_208_ALREADY_REPORTED, detail=f"Already user with ID {id} is an administrator.")
            
            temp = {
                "id": id,
                "email": user_first.email,
                "fname": user_first.fname,
                "mname": user_first.mname,
                "lname": user_first.lname,
                "password": user_first.password,
                "dateofbirth": user_first.dateofbirth,
                "role": "admin",
                "created_at":user_first.created_at,
                "phone_number":user_first.phone_number,
            }
            user.update(temp, synchronize_session=False)
            db.commit()
            

            mAdmin.user_id = id
            mAdmin.salary = 5000
            
            makingAdmin = models.Admin(**mAdmin.dict()) 
            db.add(makingAdmin)
            db.commit()
            db.refresh(makingAdmin)
            
            return {"detail": f"User with ID {id} is now an administrator."}
            
        except:
            if not user:
                raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"There is no Users.")
            
            if user_first.role == "admin":
                raise HTTPException(status_code=HTTP_208_ALREADY_REPORTED, detail=f"Already user with ID {id} is an administrator.")    
    
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=f"you don't have an administrator privileges")

@router.delete("/admin/{id}", status_code=HTTP_204_NO_CONTENT) #delete
def delete_admin(id:int, dAdmin: Optional[schemas.UserUpdateRoleREQ], db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    admin_flag = False
    
    
    if current_user.role == "root":
        admin_flag = True
    
    if admin_flag:
        user_query = db.query(models.Admin).filter(models.Admin.user_id == id)
        user = user_query.first()
        
        if not user:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no user with id {id} exist.")
        
        if user.role == "root":
            return Response(status_code=HTTP_403_FORBIDDEN)
        
        user_query.delete(synchronize_session=False)
        db.commit()
        
        
        
        dAdmin.role = "user"
        
        user_query = db.query(models.User).filter(models.User.id == id)
        user = user_query.first()
        
        if not user:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"There is no user with id {id} exist.")
        
        user.role = "user"
        
        user_query.update(dAdmin.dict(), synchronize_session=False)
        db.commit()
        
        
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=f"you don't have an root privileges")


