from fastapi.security.oauth2 import OAuth2
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app import database, models
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret_key
# Algorithm
# Exporation time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    
    temp_data = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    temp_data.update({"exp":expire})
    temp_jwt = jwt.encode(temp_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return temp_jwt



def verify_access_token(token: str, credential_exception):
    
    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
            raise credential_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token has been expired.", headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user


