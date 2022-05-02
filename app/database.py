from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
    
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<pass>@<ip>/<database name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_name}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_username}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
    
    
    
# This class just for manage the connection from/to the Database.
