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



class UserDAL:
    """Data Access Layer for operating user info"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    
    

    async def create_user(
        self,user_name: str, photo_base64: str) -> UserInDB:
        
        embeding = await base64_to_embedding(photo_base64)
        
        new_user = UserInDB(
            user_name = user_name,
            face_embeding = embeding

        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def build_index(self):
        # Отримання векторів облич з бази даних
        embeddings = []
        for user in self.db_session.query(UserInDB).all():
            embeddings.append(user.face_embedding)

        # Побудова індексу векторів облич
        index = faiss.IndexFlatIP(len(embeddings[0]))
        # embeddings = np.array([e.vector for e in embeddings]).astype('float32')
        embeddings = np.array(embeddings, dtype=np.float32)
        index.add(embeddings)
        return index


    async def get_user_by_embedding(self, embedding:  Vector) -> Union[UserInDB, None]:
         
        # user = self.db_session.query(UserInDB).order_by(UserInDB.face_embeding.l2_distance(embedding)).limit(1).all()
      

        # try:
        #     stmt = select(UserInDB).order_by(UserInDB.face_embeding.l2_distance(embedding[0])).first()
            
        #     result = await self.db_session.execute(stmt)
        #     user = result.scalar()
            
        #     return user
        
        # except:
        #     return
           



        # Отримання векторів облич з бази даних
        embeddings = []

        try:
            stmt_ = select(UserInDB.face_embeding)

            result = await self.db_session.execute(stmt_)

            embeddings = [row[0] for row in result]

        except asyncpg.exceptions.PostgresError as e:
            raise HTTPException(e, detail="Can't getting embeddings for indexation",
        )
        if len(embeddings) == 0:
            return None
        # Побудова індексу векторів облич
        index = faiss.IndexFlatL2(len(embeddings[0]))
     
        embeddings = np.array(embeddings, dtype=np.float32)
        index.add(embeddings)

        embedding_ = np.array([embedding], dtype=np.float32)

        distances_squared, indices = index.search(embedding_, k=1)

        distances = np.sqrt(distances_squared)

        if distances >= 0.5:
            return None

        try:
            stmt = select(UserInDB).where(UserInDB.user_id == indices[0][0]+1)
            result = await self.db_session.execute(stmt)
            user = result.scalar()
            return user
        
        except:
            return None
        






        # user = self.db_session.query(UserInDB).value(indices[0][0])

        # user = self.db_session.query(UserInDB).order_by(UserInDB.face_embeding.l2_distance(embedding)).limit(1).all()
        
        # try:
        #     stmt = select(UserInDB).filter(UserInDB.user_id == 'def7d118-367e-4ca9-adab-02af08428efa')
            
        #     result = await self.db_session.execute(stmt)
        #     print("RESULT" ,result)
        #     user = result.scalar()
        #     print("USER", user)
        #     return user
        
        # except:
        #     return None
        





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