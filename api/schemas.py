from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy.dialects.postgresql import UUID, ARRAY, INTEGER
from sqlalchemy import Float
import uuid
from pydantic import BaseModel
from pydantic import constr
from pydantic import EmailStr
from pgvector.sqlalchemy import Vector
from sqlalchemy import Integer
import re


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


       

class UserBase(BaseModel):
    photo_base64: str




class UserCreate(UserBase):
    user_name: str



class UserInDB(BaseModel):
    user_id: int
    user_name: str
    path_storage: str
    face_embeding: Vector
    is_active: bool

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True




class ShowUser(BaseModel):
    user_id: int
    user_name: str
    is_active: bool

    class Config:
        """tells pydantic to convert even non dict obj to json"""
        orm_mode = True

        arbitrary_types_allowed = True





class DeleteUserResponse(BaseModel):
    deleted_user_id: int
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class UpdatedUserResponse(BaseModel):
    updated_user_id: int
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True



class UpdateUserRequest(BaseModel):
    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    email: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str