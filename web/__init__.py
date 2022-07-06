import sys 

sys.dont_write_bytecode = True

import web.database

from fastapi import Depends, FastAPI

from web.auth.auth_bearer import JWTBearer
from web.routers.auth import auth as auth_router
from web.routers.graph import graph as graph_router
from web.routers.user import authenticated as auth_user_router, unauthenticated as unauth_user_router

web.database.Base.metadata.create_all(bind=web.database.engine)

app = FastAPI()

# Unauthenticated Routes
app.include_router(auth_router, prefix='/auth', tags=['auth'],)
app.include_router(unauth_user_router, prefix='/user', tags=['users'],)

# Authenticated Routes
app.include_router(graph_router, prefix='/graph', tags=['graph'], dependencies=[Depends(JWTBearer())])
app.include_router(auth_user_router, prefix='/user', tags=['users'], dependencies=[Depends(JWTBearer())])

@app.get('/')
def root():
    return {'message': 'online'}