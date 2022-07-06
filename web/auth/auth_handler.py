import os
import time

import jwt 

from typing import Dict

from web.database.schemas.user import User

JWT_SECRET = os.environ.get('JWT_SECRET')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')

def sign_jwt(user: User) -> Dict[str, str]:
    payload = {
        'uuid': user.uuid,
        'email': user.email,
        'groups': user.groups,
        'is_active': user.is_active,
        'expires': time.time() + 600
    }

    return {'access_token': jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)}


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token['expires'] >= time.time() else None
    except:
        return {}