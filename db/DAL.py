from typing import List, Union
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import update, and_, select, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import UserInDB
from pgvector.sqlalchemy import Vector
from black_box_face.base64_to_embeding import base64_to_embedding
import numpy as np
import faiss
import asyncio
import asyncpg
import os
import shutil
from datetime import datetime
import base64
from black_box_face.base64_to_embeding import path
import glob
from db import db_config_milvus

class DirectoryCreationError(Exception):
    def __init__(self, message="Cannot create directory"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"
    

class UserDAL:
    """Data Access Layer for operating user info"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session


    async def create_user(self,user_name: str, photo_base64: str, user_age: int, face_emb: list) -> UserInDB:
        
        # embeding = await base64_to_embedding(photo_base64)
        
        new_user = UserInDB(
            user_name = user_name,
            user_age = user_age
        )
        self.db_session.add(new_user)
        await self.db_session.flush()

        db_config_milvus.create_collections_if_not_exist(db_config_milvus.connection, f"_{new_user.user_id}")
        
        status, count_emb = db_config_milvus.connection.count_entities(f"_{new_user.user_id}")

        status, ids = db_config_milvus.connection.insert(
            collection_name = f"_{new_user.user_id}",
            records = [face_emb],
            ids=[count_emb])  
        db_config_milvus.connection.flush([f"_{new_user.user_id}"])

        status, ids = db_config_milvus.connection.insert(
            collection_name = "cluster",
            records = [face_emb],
            ids=[new_user.user_id])
        
        db_config_milvus.connection.flush(["cluster"])


        try:

            destination_folder = f"data/{new_user.user_id}"

            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            num_photos = len(glob.glob(os.path.join(destination_folder, "*.jpeg")))
                            
            path_new = f'data/{num_photos}.jpeg'

            os.rename(path, path_new)

            image_path = path_new

            shutil.move(image_path, destination_folder)

            new_user.path_storage = destination_folder

            self.db_session.add(new_user)
            await self.db_session.flush()

            return new_user
        
        except OSError:
            temp = new_user.user_id
            await self.db_session.rollback()
            raise HTTPException(status_code=503, detail=f"Cannot create directory {temp}")



    async def get_user_by_embedding(self, embedding:  list) -> Union[UserInDB, None]: 

        if embedding == []:
            raise HTTPException(status_code=410, detail="Did not found face, try again")
        
        search_param = {'nprobe': 16}
        param = {
                'collection_name': "cluster",
                'query_records': [embedding], 
                'top_k': 1,
                'params': search_param,
        }
        try:
            status, results = db_config_milvus.connection.search(**param)
    
        except:
            raise HTTPException(status_code=414, detail="Did not found face, try again")
    
        if len(results) == 0:
            return None

        print(f"Cosine distance: {1 - results[0][0].distance}  INDICIES: {results[0][0].id}")

        if (1 - results[0][0].distance > 0.353):
                    return None
        try:
            stmt = select(UserInDB).where(UserInDB.user_id == results[0][0].id)
            result = await self.db_session.execute(stmt)
            user = result.scalar()
            return user
        
        except:
            return None
    

    async def get_user_by_id(self, id:  int) -> Union[UserInDB, None]: 
        try:
            stmt = select(UserInDB).where(UserInDB.user_id == id)
            result = await self.db_session.execute(stmt)
            user = result.scalar()
            return user
        except:
            return None

        



    async def delete_user(self, user_id: UUID) -> Union[UUID,None]:
        query = update(UserInDB).\
            where(and_(UserInDB.user_id == user_id, UserInDB.is_active == True)).\
            values(is_active=False).\
            returning(UserInDB.user_id)

        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

# def create_user(db: Session, user: schemas.UserCreate):
#     """Створити нового користувача в базі даних."""
#     db_user = models.User(name=user.name, embedding=user.embedding)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user