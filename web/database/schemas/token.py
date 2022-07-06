from pydantic import BaseModel

class Token(BaseModel):
    access_token: str

    class Config:
        orm_mode = True

class InvalidToken(Token):
    expire_time: float

    class Config:
        orm_mode = True
