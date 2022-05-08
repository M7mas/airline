# Command to run the API: uvicorn main:app --port 8888 --reload
# This API for AirLine Project

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, get_db
from starlette.status import *
from typing import List
from app.routers import auth, blacklist, card, classes, fine, flight, maintenance, order, plane, price, reports, seat, state, ticket, type, user, waitlist, weight


app = FastAPI(
    title= "Air Line API",
    version= "1.0.0",
    description= "API - Project ICS-324 - Air Line System",
    redoc_url="/documentation",
    docs_url=None,
    openapi_url="/openAPI",
)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(blacklist.router)
app.include_router(card.router)
app.include_router(classes.router)
app.include_router(fine.router)
app.include_router(flight.router)
app.include_router(maintenance.router)
app.include_router(order.router)
app.include_router(plane.router)
app.include_router(price.router)
app.include_router(reports.router)
app.include_router(seat.router)
app.include_router(state.router)
app.include_router(ticket.router)
app.include_router(type.router)
app.include_router(user.router)
app.include_router(waitlist.router)
app.include_router(weight.router)


@app.get("/")
def main():
    return {
            "Information": "This API for Air Line Application.",
            "documentation": "/documentation",
            "OpenAPI schema ": "/openAPI",
            }







