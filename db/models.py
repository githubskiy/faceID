from sqlalchemy import Column, String, Integer, Text, DateTime, Float, Boolean, ARRAY, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
import uuid
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserInDB(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True, unique=True)
    # user_id = Column(Integer, primary_key=True, index=True, unique=True)
    user_name = Column(String, nullable=False)
    path_storage = Column(String, default="---")
    # face_embeding = Column(ARRAY(DECIMAL(13, 12)))
    face_embeding = Column(Vector(dim=8), nullable=True)
    # face_embeding = Column(Vector(dim=128))
    is_active = Column(Boolean(), default=True)
    