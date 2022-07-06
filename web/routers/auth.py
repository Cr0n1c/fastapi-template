
import argon2

import web.database.crud as crud
import web.database.schemas as schemas

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from web.database import get_db
from web.auth.auth_handler import sign_jwt
from web.database.crud.token import set_invalid_token, get_invalid_tokens

auth = APIRouter()

@auth.post('/login')
async def user_login(user: schemas.user.UserLogin, db: Session=Depends(get_db)):
    db_user = crud.user.get_user_by_email(db, email=user.email)
    error_message = 'User/Password combo not found'

    if db_user is None:
        raise HTTPException(status_code=401, detail=error_message)

    try:
        argon2.PasswordHasher().verify(db_user.hashed_password, user.password)
    except argon2.exceptions.VerifyMismatchError:
        raise HTTPException(status_code=401, detail=error_message)
    else:
        return sign_jwt(db_user)

@auth.post('/logout')
async def user_logout(user_jwt: str, response_model=schemas.token.Token, db: Session=Depends(get_db)):
    set_invalid_token(db, user_jwt)
    return {'message': 'Logged Out'}
