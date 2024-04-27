import face_recognition
import cv2
import numpy as np
import base64
from datetime import datetime
from pgvector.sqlalchemy import Vector

import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image

img_name = f"image{datetime.now()}.jpeg"

path = f'/home/hell/prog/New_Folder/fast_train/data/image{datetime.now()}'

async def base64_to_embedding(image_base64: str):
    photo = image_base64[23:]
    photo_decode = base64.b64decode(photo)
    
   
    with open(path, 'wb') as f:
        f.write(photo_decode)

   
    return await get_embeding_arc(path)
    
# async def base64_to_embedding(image_base64: str):
#     return [5,112,3,8.2234,15881,71,113.1,1]
    

async def get_embeding(image_path: str):

    current_image = face_recognition.load_image_file(image_path)

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(current_image)
    face_encodings = face_recognition.face_encodings(current_image, face_locations)

    if face_encodings:
        return face_encodings[0]
        # return face_encodings[0].tolist()
    else:
        return []
    

async def get_embeding_arc(image_name: str):
    app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_size=(640, 640))
    img = ins_get_image(image_name)
    faces = app.get(img)

    handler = insightface.model_zoo.get_model('buffalo_l')
    handler.prepare(ctx_id=0)

    if faces:
        emb = handler.get(img, faces[0])
        emb /= np.linalg.norm(emb)
        return emb.tolist()
    else:
        return []