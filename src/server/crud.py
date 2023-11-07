from sqlalchemy.orm import Session
from sqlalchemy import text
import bcrypt
import models
import schemas

def hash_password(password: str) -> str:
    """Hash passwords before saving them in the database. Don't save passwords in plain text in the database"""
    password = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(user_password, bcrypt.gensalt(rounds=12))  # You can specify the number of hashing rounds
    return hashed_password

def create_user(db: Session, user: schemas.User):
    """Add a new user to the database"""
    user.password = hash_password(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db: Session, user: schemas.User):
    """Get the data of an existing user based on username and password"""
    user.password = hash_password(user.password)
    return db.query(models.User).filter(User.username==user.username, User.password==user.password).first()