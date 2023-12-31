import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    user_type: str

    class Config:
        from_attributes=True

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes=True

class UserUsernamePasswordUserType(UserBase):
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

class UserUpdateUserType(BaseModel):
    id: int
    user_type: str

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

    class Config:
        from_attributes=True

class TicketClose(BaseModel):
    id: int
    closed_by: int

    class Config:
        from_attributes=True

class TicketFull(TicketId):
    description: str
    date_created: datetime.date
    date_closed: datetime.date | None
    closed_by: int | None
    user_id: int
    done: bool

    class Config:
        from_attributes=True