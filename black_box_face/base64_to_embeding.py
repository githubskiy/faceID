import face_recognition
import cv2
import numpy as np
import base64
from datetime import datetime
from pgvector.sqlalchemy import Vector
# def base64_to_embedding(image_base64: str):
#     photo = image_base64[23:]
#     photo_decode = base64.b64decode(photo)
#     path = 'data/image'+str(datetime.now())+'.jpeg'
#     with open(path, 'wb') as f:
#         f.write(photo_decode)
    
#     return get_embeding(path)
    
async def base64_to_embedding(image_base64: str):
    return [151,112,3,8.2234,15,67,113.1,1]
    

def get_embeding(image_path: str):

    current_image = face_recognition.load_image_file(image_path)
    #
    # # Resize frame of video to 1/4 size for faster face recognition processing
    # small_frame = cv2.resize(current_image, (0, 0), fx=0.25, fy=0.25)
    #
    # # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    # rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(current_image)
    face_encodings = face_recognition.face_encodings(current_image, face_locations)

    if face_encodings:
        return face_encodings[0]
        # return face_encodings[0].tolist()
    else:
        return 0