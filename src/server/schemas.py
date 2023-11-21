import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str

    class Config:
        from_attributes=True

class UserUsernamePassword(UserBase):
    password: str

    class Config:
        from_attributes=True

class UserUserId(BaseModel):
    id: int

    class Config:
        from_attributes=True

class UserUsernameId(UserBase):
    id: int

    class Config:
        from_attributes=True

class TicketId(BaseModel):
    id: int

    class Config:
        from_attributes=True

class TicketCreate(BaseModel):
    user_id: int
    description: str

    class Config:
        from_attributes=True

class TicketUpdate(BaseModel):
    id: int
    description: str
    done: bool

    class Config:
        from_attributes=True

class TicketFull(TicketId):
    description: str
    date_created: datetime.date
    user_id: int
    done: bool

    class Config:
        from_attributes=True