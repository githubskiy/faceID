# -*- coding: utf-8 -*-
from os import environ
from settings import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator


# DB_USER = environ.get('DB_USER', 'stas')
# DB_PASSWORD = environ.get('DB_PASS', '1131')
# DB_HOST = environ.get('DB_HOST', 'localhost')
# DB_NAME = environ.get('DB_NAME', 'new_db')
#
# DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}'

# databases query builder
# database = Database(DATABASE_URL)


engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

async_session_local = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)




async def get_db() -> Generator:
    """Dependency for getting async session"""

    try:
        db_session: AsyncSession = async_session_local()
        yield db_session
    finally:
        await db_session.close()