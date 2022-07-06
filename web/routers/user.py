import argon2

import web.database.crud as crud
import web.database.schemas as schemas

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from web.database import get_db

authenticated = APIRouter()
unauthenticated = APIRouter()

@authenticated.get('/', response_model=list[schemas.user.User])
def read_users(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    users = crud.user.get_users(db, skip=skip, limit=limit)
    return users

@authenticated.get('/{user_id}', response_model=schemas.user.User)
def read_user(user_id: int, db: Session=Depends(get_db)):
    db_user = crud.user.get_user(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    return db_user

@authenticated.get('/{user_id}/{password}', response_model=schemas.user.User)
def read_user_with_password(user_id: int, password: str, db: Session=Depends(get_db)):
    db_user = crud.user.get_user_by_id(db, user_id=user_id)
    error_message = 'User/Password combo not found'

    if db_user is None:
        raise HTTPException(status_code=404, detail=error_message)

    try:
        argon2.PasswordHasher().verify(db_user.hashed_password, password)
    except argon2.exceptions.VerifyMismatchError:
        raise HTTPException(status_code=404, detail=error_message)
    else:
        return db_user

@unauthenticated.post('/create', response_model=schemas.user.User)
def create_user(user: schemas.user.UserCreate, db: Session=Depends(get_db)):
    db_user = crud.user.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    
    return crud.user.create_user(db=db, user=user)

