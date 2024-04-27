from sqlalchemy import Column, String, Integer, Text, DateTime, Float, Boolean, ARRAY, DECIMAL
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserInDB(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True, unique=True)
    user_name = Column(String, nullable=False)
    path_storage = Column(String, default="---")
    user_age =  Column(Integer, nullable=False)
    is_active = Column(Boolean(), default=True)
    