import crud
import models
import schemas

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/get")
def get_user(user: schemas.User, db: Session = Depends(get_db)):
    """Try to get user data from the database using username and password. If the user isn't found or if the credentials are wrong, return a 404 HTTP error"""
    user = crud.get_user(db, user)

    if user is None:
        return HTTPException(status_code=404, detail="User not found or wrong credentials.")
    else:
        return user

@app.post("/users/new")
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    """Create a new user in the database. If the user already exists, return 400 error"""
    user = crud.get_user(db, user)

    if user is not None:
        return HTTPException(status_code=400, detail="Something went wrong when creating the user. The username might already exist in the database.")

    new_user = crud.get_user(db, user)

    if user is None:
        return HTTPException(status_code=404, detail="Something went wrong when creating the user")
    else:
        return user