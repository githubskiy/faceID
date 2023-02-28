from sqlalchemy import Integer
from typing import List, Union

from api.schemas import UserInDB, UserCreate, ShowUser
from db.db_config import async_session_local
from db.DAL import UserDAL


async def _create_new_user(body: UserCreate, db)-> ShowUser:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)

            user = await user_dal.create_user(
                user_name = body.user_name,
                photo_base64 = body.photo_base64
            )
            return ShowUser(
                user_id=user.user_id,
                user_name=user.user_name,
                is_active=user.is_active
            )

async def _delete_user(user_id, db) -> Union[Integer, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            deleted_user_id = await user_dal.delete_user(
                user_id=user_id
            )
            return deleted_user_id


async def _update_user(
    updated_user_params: dict, user_id: Integer, session
) -> Union[Integer, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user_id = await user_dal.update_user(
            user_id=user_id, **updated_user_params
        )
        return updated_user_id


async def _get_user_by_id(user_id, session) -> Union[ShowUser, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(
            user_id=user_id,
        )
        if user is not None:
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                is_active=user.is_active,
            )
