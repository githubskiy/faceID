from typing import Union
from logging import getLogger
from pydantic import BaseModel
from fastapi import FastAPI, Query,Request
from fastapi.routing import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .schemas import *
from db.db_config import async_session_local
from api.service.user import _create_new_user, _delete_user, _update_user, _get_user_by_id
from jose import jwt
from settings.settings import *
from db.db_config import get_db
from api.service.auth import authenticate_user
from api.service.user_info import get_user
from black_box_face.base64_to_embeding import base64_to_embedding
from db import db_config_milvus
from fastapi import Body

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    face_emb = await base64_to_embedding(body.photo_base64)
    user_or_none = await authenticate_user(face_emb, db)

    if user_or_none:
        raise HTTPException(status_code=409, detail="User with this username already exists")
    try:
        return await _create_new_user(face_emb=face_emb, body=body, db=db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    

@user_router.get("/info")
async def get_user_by_token(request: Request, db: AsyncSession = Depends(get_db)):

    # Отримання токену доступу з заголовка Authorization
    auth_header = request.headers.get("Authorization")
    if auth_header is None or not auth_header.startswith("Bearer "):
        # Помилка, якщо заголовок Authorization не містить токен доступу
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    token = auth_header.replace("Bearer ", "")

    # Отримання даних користувача з маршруту "/user/info" за допомогою токену доступу
    # try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    # except jwt.exceptions.InvalidTokenError:
    #     raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    user_id = int(user_id)

    user = await get_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user




# @user_router.delete("/", response_model=DeleteUserResponse)
# async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db), 
#                         current_user: UserInDB = Depends(get_current_user_from_token),
#                     ) -> DeleteUserResponse:

#     deleted_user_id = await _delete_user(user_id, db)
#     if deleted_user_id is None:
#         raise HTTPException(
#             status_code=404, detail=f"User with id {user_id} not found."
#         )
#     return DeleteUserResponse(deleted_user_id=deleted_user_id)


# @user_router.get("/", response_model=ShowUser)
# async def get_user_by_id(
#     user_id: UUID,
#     db: AsyncSession = Depends(get_db),
#     current_user: UserInDB = Depends(get_current_user_from_token),
# ) -> ShowUser:
#     user = await _get_user_by_id(user_id, db)
#     if user is None:
#         raise HTTPException(
#             status_code=404, detail=f"User with id {user_id} not found."
#         )
#     return user


# @user_router.patch("/", response_model=UpdatedUserResponse)
# async def update_user_by_id(
#     user_id: UUID,
#     body: UpdateUserRequest,
#     db: AsyncSession = Depends(get_db),
#     current_user: UserInDB = Depends(get_current_user_from_token),
# ) -> UpdatedUserResponse:
#     updated_user_params = body.dict(exclude_none=True)
#     if updated_user_params == {}:
#         raise HTTPException(
#             status_code=422,
#             detail="At least one parameter for user update info should be provided",
#         )
#     user = await _get_user_by_id(user_id, db)
#     if user is None:
#         raise HTTPException(
#             status_code=404, detail=f"User with id {user_id} not found."
#         )
#     try:
#         updated_user_id = await _update_user(
#             updated_user_params=updated_user_params, session=db, user_id=user_id
#         )
#     except IntegrityError as err:
#         logger.error(err)
#         raise HTTPException(status_code=503, detail=f"Database error: {err}")
#     return UpdatedUserResponse(updated_user_id=updated_user_id)
