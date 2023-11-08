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

@app.get("/users/get_by/userpass")
def get_user_by_username_password(user: schemas.UserUsernamePassword, db: Session = Depends(get_db)):
    """Get user data from the database using the provided username and password. If the user isn't found or if the credentials are wrong, return a 404 HTTP error"""
    user = crud.get_user_by_username_password(db, user)

    if user is None:
        return HTTPException(status_code=404, detail="User not found or wrong credentials.")
    else:
        return schemas.UserUsernameId(username=user.username, id=user.id)

@app.get("/users/get_by/id")
def get_user_by_id(user: schemas.UserUserId, db: Session = Depends(get_db)):
    """Get user data from the database using the provided username and password. If the user isn't found or if the credentials are wrong, return a 404 HTTP error"""
    user = crud.get_user_by_id(db, user)

    if user is None:
        return HTTPException(status_code=404, detail="User not found or wrong credentials.")
    else:
        return schemas.UserUsernameId(username=user.username, id=user.id)

@app.post("/users/create")
def create_user(user: schemas.UserUsernamePassword, db: Session = Depends(get_db)):
    """Create a new user in the database. If the user already exists, return 400 error"""
    find_user = crud.get_user_by_username_password(db, user)

    if find_user is not None:
        return HTTPException(status_code=400, detail="Something went wrong when creating the user. The username might already exist in the database.")

    new_user = crud.create_user(db, user)

    if user is None:
        return HTTPException(status_code=400, detail="Something went wrong when creating the user")
    else:
        return schemas.UserUsernameId(id=new_user.id, username=new_user.username)

@app.get("/tickets/get")
def get_ticket(ticket: schemas.TicketId, db: Session = Depends(get_db)):
    """Get ticket from the database based on the provided ticket id. If the ticket couldn't be found, return a 404 error"""
    ticket = crud.get_ticket(db, ticket)

    if ticket is None:
        return HTTPException(status_code=404, detail="Ticket couldn't be found")
    else:
        return schemas.TicketFull(
            id=ticket.id,
            description=ticket.description,
            date_created=ticket.date_created,
            user_id=ticket.user_id
        )

@app.get("/tickets/get_all")
def get_ticket(db: Session = Depends(get_db)) -> list[schemas.TicketFull]:
    """Get all tickets from the database"""
    return crud.get_all_tickets(db)

@app.post("/tickets/create")
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    """Add a new ticket to the database"""
    ticket = crud.create_ticket(db, ticket)
    return schemas.TicketFull(
        id=ticket.id,
        description=ticket.description,
        date_created=ticket.date_created,
        user_id=ticket.user_id
    )

@app.put("/tickets/update")
def update_ticket(ticket: schemas.TicketUpdateDescription, db: Session = Depends(get_db)):
    """Update the description of a ticket with a certain id"""
    try:
        crud.update_ticket(db, ticket)
    except Exception as ex:
        return HTTPException(status_code=404, detail="Something went wrong when trying to update the ticket. The ID might not have been found")

@app.delete("/tickets/delete")
def delete_ticket(ticket: schemas.TicketId, db: Session = Depends(get_db)):
    """Delete ticket"""
    try:
        crud.delete_ticket(db, ticket)
    except Exception as ex:
        return HTTPException(status_code=404, detail="Something went wrong when trying to delete the ticket. The ID might not have been found")