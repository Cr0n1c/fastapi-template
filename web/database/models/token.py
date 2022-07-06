from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship

from web.database import Base

class InvalidToken(Base):
    __tablename__ = 'invalid_tokens'

    access_token = Column(String, primary_key=True, index=True)
    expire_time = Column(Float)
