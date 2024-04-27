from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from db.DAL import UserDAL
from db.models import UserInDB
from db.db_config import get_db


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


async def _get_user_by_id_for_info(id: int, session: AsyncSession):

    async with session.begin():
        user_dal = UserDAL(session)
   
        return await user_dal.get_user_by_id(id)


async def get_user(id: int, db: AsyncSession) -> Union[UserInDB, None]:
    
    user = await _get_user_by_id_for_info(id, session=db)
    
    if user is None:
        return
    return user