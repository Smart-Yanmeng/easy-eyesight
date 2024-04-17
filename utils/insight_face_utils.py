import os
from random import choice

import cv2
import insightface
import numpy as np
from sklearn import preprocessing
from sklearn.decomposition import PCA

from settings.settings import DeployConfig

model = insightface.app.FaceAnalysis()
model.prepare(ctx_id=0, det_thresh=0.45, det_size=(128, 128))
pca = PCA(n_components=4)


# 提取人脸特征
def get_feature_data(data):
    face = model.get(np.array(data))[0]
    embedding = face.embedding
    feature = embedding.reshape(32, -1)
    reduced_feature = pca.fit_transform(feature)

    return list(reduced_feature.reshape(-1))


# 从给定图像文件中提取人脸特征
def get_feature(image_path):
    face_img = cv2.imread(image_path)

    faces = model.get(face_img)[0]

    return faces


class FaceRecognition:
    def __init__(self, conf_file):
        self.config = DeployConfig(conf_file)
        # 加载人脸识别模型
        self.model = insightface.app.FaceAnalysis()
        self.model.prepare(ctx_id=self.config.gpu_id)
        # 人脸库的人脸特征
        self.faces_embedding = list()
        # 加载人脸库中的人脸
        self.load_faces(self.config.face_db)

    # 加载人脸库中的人脸
    def load_faces(self, face_db_path):

        if not os.path.exists(face_db_path):
            os.makedirs(face_db_path)

        for root, dirs, files in os.walk(face_db_path):
            for file in files:
                input_image = cv2.imdecode(np.fromfile(os.path.join(root, file), dtype=np.uint8), 1)
                user_id = file.split(".")[0]
                face = self.model.get(input_image)[0]
                embedding = np.array(face.embedding).reshape((1, -1))
                embedding = preprocessing.normalize(embedding)

                self.faces_embedding.append({
                    "user_id": user_id,
                    "feature": embedding
                })

    # def recognition(self, image):
    #     faces = self.model.get(image)
    #     results = list()
    #     for face in faces:
    #         result = dict()
    #         # 获取人脸属性
    #         result["bbox"] = np.array(face.bbox).astype(np.int32).tolist()
    #         # result["landmark"] = np.array(face.landmark).astype(np.int32).tolist()
    #         if face.landmark is not None:
    #             result["landmark"] = np.array(face.landmark).astype(np.int32).tolist()
    #         result["age"] = face.age
    #         gender = '男'
    #         if face.gender == 0:
    #             gender = '女'
    #         result["gender"] = gender
    #         # 开始人脸识别
    #         embedding = np.array(face.embedding).reshape((1, -1))
    #         embedding = preprocessing.normalize(embedding)
    #         result["user_id"] = "unknown"
    #         for com_face in self.faces_embedding:
    #             r = self.feature_compare(embedding, com_face["feature"], self.config.threshold)
    #             if r:
    #                 result["user_id"] = com_face["user_id"]
    #         results.append(result)
    #     return results

    @staticmethod
    def feature_compare(feature1, feature2, threshold):
        diff = np.subtract(feature1, feature2)
        dist = np.sum(np.square(diff), 1)
        if dist < threshold:
            return True
        else:
            return False

    def register(self, image):
        # 只允许图片中只有一张人脸
        faces = self.model.get(image)
        if len(faces) != 1:
            return None

        # 提取人脸特征
        embedding = np.array(faces[0].embedding).reshape((1, -1))
        embedding = preprocessing.normalize(embedding)

        # face_featrue = embedding.tobytes()

        # print(embedding.tobytes())
        # print(embedding.reshape((1, -1)))

        # 判断人脸是否存在数据库中
        is_exits = False

        for com_face in self.faces_embedding:
            r = self.feature_compare(embedding, com_face["feature"], self.config.threshold)
            if r:
                is_exits = True
        if is_exits:
            return None
        old_user_id = [d["user_id"] for d in self.faces_embedding]
        user_id = self.get_user_id(old_user_id)

        # 符合注册条件保存图片，同时把特征添加到人脸特征库中
        # cv2.imencode('.png', image)[1].tofile(os.path.join(self.config.face_db, '%s.png' % user_id))
        # self.faces_embedding.append({
        #     "user_id": user_id,
        #     "feature": embedding
        # })
        #
        # return user_id

    def get_user_id(self, old_user_id):
        print(old_user_id)
        while True:
            user_id = "".join([choice("0123456789ABCDEF") for i in range(8)])
            if user_id not in old_user_id:
                break
        return user_id
