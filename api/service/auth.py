from typing import Union

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from pgvector.sqlalchemy import Vector
from starlette import status
from sqlalchemy import Float
import settings
from db.DAL import UserDAL
from db.models import UserInDB
from db.db_config import get_db
from hashing import Hasher

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


async def _get_user_by_embeding_for_auth(face_embedding: Vector, session: AsyncSession):

    async with session.begin():
        user_dal = UserDAL(session)
   
        return await user_dal.get_user_by_embedding(face_embedding)


async def authenticate_user(face_embedding: Vector, db: AsyncSession) -> Union[UserInDB, None]:
    
    user = await _get_user_by_embeding_for_auth(face_embedding, session=db)
    
    if user is None:
        return
    return user


# async def get_current_user_from_token(
#     token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#     )
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
#         )
#         email: str = payload.get("sub")
#         print("username/email extracted is ", email)
#         if email is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = await _get_user_by_embeding_for_auth(email=email, session=db)
#     if user is None:
#         raise credentials_exception
#     return user
