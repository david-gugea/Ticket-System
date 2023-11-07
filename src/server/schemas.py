import datetime
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes=True

class TicketCreate(BaseModel):
    description: str
    date_created: datetime.date
    user_id: int

    class Config:
        from_attributes=True