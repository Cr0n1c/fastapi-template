import uuid

import web.database.models as models
import web.database.schemas as schemas

from argon2 import PasswordHasher

from sqlalchemy.orm import Session
from web.database import models

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.user.User).filter(models.user.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.user.User).filter(models.user.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.user.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.user.UserCreate):
    db_user = models.user.User(email=user.email, 
                               hashed_password=PasswordHasher().hash(user.password), 
                               uuid=str(uuid.uuid4()),
                               groups=user.groups
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
