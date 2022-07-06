from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserLogin(UserBase):
    password: str

class UserCreate(UserBase):
    password: str
    groups: list

class User(UserBase):
    id: int
    uuid: str
    groups: list
    is_active: bool

    class Config:
        orm_mode = True