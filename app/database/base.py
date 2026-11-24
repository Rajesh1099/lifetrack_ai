from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

#user model table imports the structure from base
from app.models.user import User 
    