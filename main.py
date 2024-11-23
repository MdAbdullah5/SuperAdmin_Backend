from fastapi import FastAPI, Form, Request, Depends, HTTPException, BackgroundTasks, UploadFile, File, Path
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, constr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from starlette.middleware.sessions import SessionMiddleware
from itsdangerous import URLSafeTimedSerializer
from database import SessionLocal, engine
from models import EventFormSubmission, User, Event, EventForm
from schemas import UserSchema, EventFormCreate, UserDetails, EventCreate
from database import Base
from datetime import date
from schemas import EventStatusEnum, FormCreate
import base64
from typing import List, Any, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from jinja2 import Template
from starlette.status import HTTP_401_UNAUTHORIZED
from functools import wraps
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from datetime import datetime, timedelta
import qrcode
from io import BytesIO
import json
import os
from uuid import UUID, uuid4
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Form, Body
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI, Request, Depends, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from starlette.responses import JSONResponse
from sqlalchemy import select

app = FastAPI()

# Add CORS middleware
origins = [
    "http://localhost:3000",  # React app URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Updated event model to include status
class Event(BaseModel):
    id: int
    name: str
    venue: str
    description: str
    date: str
    status: str  # Added status field

# Sample data with status
events_data2 = [
    Event(id=1, name="Concert", venue="Stadium", description="Live concert", date="2024-01-01", status="Pending"),
    Event(id=2, name="Art Exhibition", venue="Gallery", description="Art works exhibition", date="2024-02-15", status="Approved"),
    Event(id=3, name="Tech Conference", venue="Convention Center", description="Technology discussions", date="2024-03-10", status="Pending"),
]

app.get("/admin/event_organizers", response_model=List[User])  # Assuming you want to return a list of User models
async def get_event_organizers(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()  # Fetch all users
        return users  # Returns the list of all users
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching users.")



    

@app.get("/admin/event_status", response_model=List[Event])
async def get_eventStatus():
    return events_data2
