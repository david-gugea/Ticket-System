import hashlib
import datetime
import models
import schemas

from sqlalchemy.orm import Session
from sqlalchemy import text

def hash_password(password: str) -> str:
    """Hash passwords before saving them in the database. Don't save passwords in plain text in the database"""
    password = password.encode("utf-8")
    sha256 = hashlib.sha256(password)
    return sha256.hexdigest()

def create_user(db: Session, user: schemas.UserUsernamePassword):
    """Add a new user to the database"""
    hashed_password = hash_password(user.password)

    new_user = models.User(**user.dict())
    new_user.password = hashed_password
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username_password(db: Session, user: schemas.UserUsernamePassword):
    """Get the data of an existing user based on username and password"""
    hashed_password = hash_password(user.password)
    return db.query(models.User).filter(models.User.username==user.username, models.User.password==hashed_password).first()

def get_user_by_id(db: Session, user: schemas.UserUserId):
    """Get the data of an existing user based on username and password"""
    return db.query(models.User).filter(models.User.id == user.id).first()

def get_ticket(db: Session, ticket_id: schemas.TicketId):
    """Get the data of an existing user based on username and password"""
    return db.query(models.Ticket).filter(models.Ticket.id==ticket_id.id).first()

def get_all_tickets(db: Session):
    """Get all tickets from the database"""
    return db.query(models.Ticket).all()

def create_ticket(db: Session, ticket: schemas.TicketCreate):
    """Add a new ticket to the database"""
    new_ticket = models.Ticket(**ticket.dict())
    new_ticket.date_created = datetime.date.today()
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

def update_ticket(db: Session, ticket_update: schemas.TicketUpdateDescription):
    """Update the description of the ticket"""
    ticket = db.query(models.Ticket).filter(models.Ticket.id==ticket_update.id).first()
    ticket.description = ticket_update.description
    db.commit()

def delete_ticket(db: Session, ticket_delete: schemas.TicketId):
    """Delete ticket with the given ID"""
    ticket = db.query(models.Ticket).filter(models.Ticket.id==ticket_delete.id).delete()
    db.commit()