from sqlalchemy import Column, Integer, Float, Sequence, Text, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id=Column(Integer, primary_key=True, index=True)
    username=Column(Text, unique=True)
    password=Column(Text)
    user_type=Column(Text)
    salt=Column(Text)

    created_tickets = relationship("Ticket", foreign_keys="[Ticket.user_id]", back_populates="user")
    closed_tickets = relationship("Ticket", foreign_keys="[Ticket.closed_by]", back_populates="closed_by_user")

class Ticket(Base):
    __tablename__ = "tickets"

    id=Column(Integer, primary_key=True, index=True)
    description=Column(Text)
    date_created=Column(Date)
    date_closed=Column(Date)
    done=Column(Boolean, default=False)

    # This id represents the user who closed the ticket
    closed_by=Column(Integer, ForeignKey("users.id"))

    # Create a foreign key relationship with the User model
    # This id represents who created the ticket
    user_id=Column(Integer, ForeignKey("users.id"))

    # Define the back reference to the User model
    user = relationship("User", foreign_keys="[Ticket.user_id]", back_populates="created_tickets")
    closed_by_user = relationship("User", foreign_keys="[Ticket.closed_by]", back_populates="closed_tickets")