import hashlib
import time 

import web.database.models as models

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from web.database import models
from web.auth.auth_handler import decode_jwt

def is_token_expired(expire_ts: float, current_time: float = time.time()) -> bool:
    return current_time > expire_ts

def set_invalid_token(db: Session, access_token: str):
    decoded_token = decode_jwt(access_token)

    if not decoded_token.get('expires'):
        return False

    if is_token_expired(decoded_token['expires']):
        return True 
    
    try:
        db.add(models.token.InvalidToken(access_token=hashlib.sha256(str.encode(access_token)).hexdigest(), 
                                         expire_time=decoded_token['expires'])
        )
        db.commit()
    except IntegrityError:
        db.flush()
        db.rollback()
    
    return True

def get_invalid_tokens(db: Session):
    cleanup_tokens(db)
    return db.query(models.token.InvalidToken).all()

def is_valid_token(db: Session, access_token: str):
    hashed_access_token = hashlib.sha256(str.encode(access_token)).hexdigest()
    if db.query(models.token.InvalidToken).filter(models.token.InvalidToken.access_token == hashed_access_token).first():
        return False
    else:
        return True


def cleanup_tokens(db: Session):
    db.query(models.token.InvalidToken).filter(models.token.InvalidToken.expire_time < time.time()).delete()

