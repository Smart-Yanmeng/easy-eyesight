import warnings
import numpy as np
import aface
from peewee import *

# 忽略警告信息
warnings.filterwarnings("ignore", category=DeprecationWarning)

db = SqliteDatabase('faces.db')


class FaceModel(Model):
    name = CharField()
    feature = BlobField()

    class Meta:
        database = db


class Face_service:
    def __init__(self):
        db.create_tables([FaceModel])

    # 添加人脸
    def add_face(self, img_data, user_name):
        try:
            encodings = np.array(aface.get_feature_data(img_data))
            face = FaceModel(name=user_name, feature=encodings.tobytes())
            face.save()
            return True
        except Exception as e:
            print(e)
            return False

    def search_face_line(self, img_data):
        try:
            search_encoding = aface.get_feature_data(img_data)
            results = []
            for face in FaceModel.select():
                encoding = np.frombuffer(face.feature, dtype=np.float32)
                distance = np.linalg.norm(search_encoding - encoding)
                results.append((face.id, face.name, distance))
            results = sorted(results, key=lambda x: x[2])
            if (len(results) == 0):
                return []
            return results[0]
        except Exception as e:
            print(e)
            return False

    def get_faces(self):
        data = [{"id": face.id, "name": face.name} for face in FaceModel.select()]
        return data

    def delete_face_by_id(self, id):
        FaceModel.get_by_id(id).delete_instance()
