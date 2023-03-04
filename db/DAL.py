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

    
    

    async def create_user(
        self,user_name: str, photo_base64: str, face_emb: Vector) -> UserInDB:
        
        # embeding = await base64_to_embedding(photo_base64)
        
        new_user = UserInDB(
            user_name = user_name,
            face_embeding = face_emb

        )
        self.db_session.add(new_user)
        await self.db_session.flush()


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



    async def get_user_by_embedding(self, embedding:  Vector) -> Union[UserInDB, None]: 

        if embedding == []:
            raise HTTPException(status_code=410, detail="Did not found face, try again")

        # Отримання векторів облич з бази даних
        embeddings = []

        try:
            stmt_vec = select(UserInDB.face_embeding)
           
            result_vec = await self.db_session.execute(stmt_vec)


            embeddings = [row[0] for row in result_vec]
           

            embeddings = np.array(embeddings, dtype=np.float32)

        except asyncpg.exceptions.PostgresError as e:
            raise HTTPException(e, detail="Can't getting embeddings for indexation",
        )
        if len(embeddings) == 0:
            return None
        

         # Normalize the vectors
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

        # Побудова індексу векторів облич
        index = faiss.IndexFlatIP(len(embeddings[0]))

        # index_description = "IVF{x},Flat".format(x=1)

        # index = faiss.index_factory(len(embeddings[0]), index_description, faiss.METRIC_INNER_PRODUCT)
        # ids = np.array(ids)
        # index.train(embeddings)


        index.add(embeddings)


        query_embedding = np.array([embedding], dtype=np.float32)

        query_embedding /= np.linalg.norm(query_embedding) 

        # distances_squared, indices = index.search(query_embedding, k=1)

        # distances = np.sqrt(distances_squared)

        distances, indices = index.search(query_embedding, k=1)

        cosine_distance = 1.0 - distances[0][0]
        
        print(f"SIMILARITY: {distances}  INDICIES: {indices}")
        print(f"COSINE DISTANCE: {cosine_distance}  INDICIES: {indices}")

        if cosine_distance >= 0.1:
            return None

        try:
            stmt = select(UserInDB).where(UserInDB.user_id == indices[0][0]+1)
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