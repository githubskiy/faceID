from datetime import timedelta
from typing import Union
from logging import getLogger
from pydantic import BaseModel
from fastapi import FastAPI, Query
from fastapi.routing import APIRouter
from fastapi import status
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .schemas import *
from settings.settings import *
from db.db_config import async_session_local
from api.service.user import _create_new_user, _delete_user, _update_user, _get_user_by_id
from security import create_access_token
from db.db_config import get_db
from api.service.auth import authenticate_user
from black_box_face.base64_to_embeding import base64_to_embedding
from fastapi.security import OAuth2PasswordRequestForm
from black_box_face.base64_to_embeding import path
import os
import shutil
import glob
from db import db_config_milvus
import numpy as np

login_router = APIRouter()

@login_router.post("/", response_model=Token)
async def login_for_access_token(form_data: UserBase , db: AsyncSession = Depends(get_db)):

    face_emb = await base64_to_embedding(form_data.photo_base64)

    # print("FACEEE EMMBEDDINGG", face_emb)
    user_or_none = await authenticate_user(face_emb, db)

    if user_or_none is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
        )
    else:
        # add face_emb to user_or_none.user_id collection/ можливо потрібно винести у функцію, десь до бд
        status_, count_emb = db_config_milvus.connection.count_entities(f"_{user_or_none.user_id}")
        
        #перед інсертом можливо потрібно зробити перевірку та видалити ентіті за айді
        status_, ids = db_config_milvus.connection.insert(
                    collection_name = f"_{user_or_none.user_id}",
                    records = [face_emb],
                    ids=[count_emb])  
        db_config_milvus.connection.flush([f"_{user_or_none.user_id}"])

        status_, count_emb = db_config_milvus.connection.count_entities(f"_{user_or_none.user_id}")
        status_, result_vectors = db_config_milvus.connection.get_entity_by_id(
            f"_{user_or_none.user_id}", 
            [i for i in range(count_emb)])
        
        mean_vector = np.mean(result_vectors, axis=0)
        mean_vector = mean_vector.tolist()
        db_config_milvus.connection.delete_entity_by_id(collection_name="cluster", id_array=[user_or_none.user_id])
        status_, ids = db_config_milvus.connection.insert(
                collection_name = "cluster",
                records = [mean_vector],
                ids=[user_or_none.user_id])
        db_config_milvus.connection.flush([f"_{user_or_none.user_id}"])
        # print(mean_vector[:10], "... added to cluster by ", user_or_none.user_id, "idx")
    
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        data={"sub": str(user_or_none.user_id), "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )

    if access_token:

        # можливо пізніш потрібно виокремити у функцію код нижче, а також може кидати ексепш коли токен не створиться
        destination_folder = f"data/{user_or_none.user_id}"

        # if not os.path.exists(destination_folder):
        #     os.makedirs(destination_folder)

        num_photos = len(glob.glob(os.path.join(destination_folder, "*.jpeg")))

        path_new = f'data/{num_photos}.jpeg'

        os.rename(path, path_new)

        image_path = path_new

        shutil.move(image_path, destination_folder)


    return {"access_token": access_token, "token_type": "bearer"}