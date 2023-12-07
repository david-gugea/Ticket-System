import secrets
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

def gen_salt() -> str:
    return secrets.token_hex(16)

def create_user(db: Session, user: schemas.UserUsernamePassword):
    """Add a new user to the database"""
    new_user = models.User(**user.dict())
    salt = gen_salt()
    hashed_password = hash_password(f"{user.password}:{salt}")
    new_user.password = hashed_password
    new_user.salt = salt
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username_password(db: Session, user: schemas.UserUsernamePassword):
    """Get the data of an existing user based on username and password"""
    db_user = db.query(models.User).filter(models.User.username==user.username).first()

    if db_user is None:
        # wrong username
        return None

    print(f"get_user_by_username_password user -> {user} || {type(user)}")
    salt_value = db_user.salt
    hashed_password = hash_password(f"{user.password}:{salt_value}")
    print(f"salt_value -> {db_user.salt} | hashed_password -> {hashed_password}")

    if hashed_password != db_user.password:
        # wrong password
        return None
    else:
        return db_user

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

def close_ticket(db: Session, ticket_close: schemas.TicketClose):
    """Close a ticket"""
    ticket = db.query(models.Ticket).filter(models.Ticket.id==ticket_close.id).first()
    print(f"TICKET CLOSE TICKET -> {ticket}")
    ticket.done = True
    ticket.closed_by = ticket_close.closed_by
    ticket.date_closed = datetime.date.today()
    db.commit()

    return ticket

def update_ticket(db: Session, ticket_update: schemas.TicketUpdate):
    """Update the description/done status of the ticket"""
    ticket = db.query(models.Ticket).filter(models.Ticket.id==ticket_update.id).first()
    ticket.description = ticket_update.description
    db.commit()

    return ticket

def delete_ticket(db: Session, ticket_delete: schemas.TicketId):
    """Delete ticket with the given ID"""
    ticket = db.query(models.Ticket).filter(models.Ticket.id==ticket_delete.id).delete()
    db.commit()