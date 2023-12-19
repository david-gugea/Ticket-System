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
def get_user_by_username_password(username: str, password: str, db: Session = Depends(get_db)):
    """Get user data from the database using the provided username and password. If the user isn't found or if the credentials are wrong, return a 404 HTTP error"""
    user = crud.get_user_by_username_password(db, username, password)

    if user is None:
        return HTTPException(status_code=404, detail="User not found or wrong credentials.")
    else:
        return schemas.UserUsernameId(username=user.username, id=user.id, user_type=user.user_type)

@app.get("/users/get_by/id")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Get user data from the database using the provided username and password. If the user isn't found or if the credentials are wrong, return a 404 HTTP error"""
    user = crud.get_user_by_id(db, user_id)

    if user is None:
        return HTTPException(status_code=404, detail="User not found or wrong credentials.")
    else:
        return schemas.UserUsernameId(username=user.username, id=user.id, user_type=user.user_type)

@app.post("/users/create")
def create_user(user: schemas.UserUsernamePasswordUserType, db: Session = Depends(get_db)):
    """Create a new user in the database. If the user already exists, return 400 error"""
    find_user = crud.get_user_by_username_password(db, user.username, user.password)

    if find_user is not None:
        return HTTPException(status_code=400, detail="Something went wrong when creating the user. The username might already exist in the database.")

    new_user = crud.create_user(db, user)

    if user is None:
        return HTTPException(status_code=400, detail="Something went wrong when creating the user")
    else:
        return schemas.UserUsernameId(id=new_user.id, username=new_user.username, user_type=new_user.user_type)

@app.get("/users/get_all")
def get_all_users(db: Session = Depends(get_db)):
    """Get all users"""
    users = crud.get_all_users(db)
    user_out_list: list[schemas.UserOut] = []
    for user in users:
        user_out_list.append(
            schemas.UserOut(
                id=user.id,
                username=user.username,
                user_type=user.user_type,
            )
        )

    return user_out_list

@app.put("/users/update_user_type")
def update_user_type(update_user_type_schema: schemas.UserUpdateUserType, db: Session = Depends(get_db)):
    """Change the type of the user with the provided user id"""

    updated_user = crud.update_user_type(update_user_type_schema, db)
    return schemas.UserOut(
        id=updated_user.id,
        username=updated_user.username,
        user_type=updated_user.user_type,
    )

@app.get("/tickets/get")
def get_ticket_by_id(ticket_id: int, db: Session = Depends(get_db)):
    """Get ticket from the database based on the provided ticket id. If the ticket couldn't be found, return a 404 error"""
    ticket = crud.get_ticket(db, ticket_id)

    if ticket is None:
        return HTTPException(status_code=404, detail="Ticket couldn't be found")
    else:
        return schemas.TicketFull(
            id=ticket.id,
            description=ticket.description,
            date_created=ticket.date_created,
            user_id=ticket.user_id,
            done=ticket.done,
            date_closed = ticket.date_closed,
            closed_by = ticket.closed_by,
        )

@app.get("/tickets/get_all")
def get_all_tickets(db: Session = Depends(get_db)) -> list[schemas.TicketFull]:
    """Get all tickets from the database"""
    return crud.get_all_tickets(db)

@app.get("/tickets/get_by_user_id")
def get_tickets_with_user_id(user_id: int, db: Session = Depends(get_db)) -> list[schemas.TicketFull]:
    """Get all tickets that have a certain user id"""
    return crud.get_all_tickets_by_user_id(user_id, db)

@app.post("/tickets/create")
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    """Add a new ticket to the database"""
    ticket = crud.create_ticket(db, ticket)
    return schemas.TicketFull(
        id=ticket.id,
        description=ticket.description,
        date_created=ticket.date_created,
        user_id=ticket.user_id,
        done=ticket.done,
        date_closed=None,
        closed_by=None
    )

@app.put("/tickets/update")
def update_ticket(ticket: schemas.TicketUpdate, db: Session = Depends(get_db)):
    """Update the description of a ticket with a certain id"""
    try:
        crud.update_ticket(db, ticket)
    except Exception as ex:
        return HTTPException(status_code=404, detail="Something went wrong when trying to update the ticket. The ID might not have been found")

@app.put("/tickets/close")
def close_ticket(ticket: schemas.TicketClose, db: Session=Depends(get_db)):
    """Set a ticket's done status to true and save the id of the user who closed the ticket and the data when this happened"""
    try:
        crud.close_ticket(db, ticket)
    except Exception as ex:
        print(ex)
        return HTTPException(status_code=404, detail="Something went wrong when trying to close the ticket. The ID of the ticket or the ID of the user that closed the ticket might not have been found")

@app.delete("/tickets/delete")
def delete_ticket(ticket: schemas.TicketId, db: Session = Depends(get_db)):
    """Delete ticket"""
    try:
        crud.delete_ticket(db, ticket)
    except Exception as ex:
        return HTTPException(status_code=404, detail="Something went wrong when trying to delete the ticket. The ID might not have been found")