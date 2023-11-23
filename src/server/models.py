from sqlalchemy import Column, Integer, Float, Sequence, Text, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id=Column(Integer, primary_key=True, index=True)
    username=Column(Text)
    password=Column(Text)

    tickets=relationship("Ticket", back_populates="user")

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
    owner_id=Column(Integer, ForeignKey("users.id"))

    # Define the back reference to the User model
    user = relationship("User", back_populates="tickets")