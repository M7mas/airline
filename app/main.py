# Command to run the API: uvicorn main:app --port 8888 --reload
# This API for AirLine Project


from http.client import HTTPException
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import models, schemas
from app.routers import Temp, user, auth
from app.database import engine, get_db
from starlette.status import *
from typing import List


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Temp.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def main():
    return {"message": "This API for Air Line Application."}







