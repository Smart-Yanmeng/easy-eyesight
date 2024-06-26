import os

import cv2

import numpy as np
from sklearn import preprocessing

from costom_error import *
from pojo.po_models import User
from service import config
from settings.face_model import FaceModel
from utils.capture_utils import get_frame

model = FaceModel.get_model()


async def load_face():
    """
    :introduction 加载所有人脸数据
    """

    faces = await User.all()
    results = list()
    result = dict()

    for face in faces:
        result["user_id"] = face.user_id
        result["username"] = face.username
        result["face_image"] = face.face_img

        results.append(result)

    return results


class UserService:
    def __init__(self):
        print("初始化 FaceService ...")

    @staticmethod
    def feature_compare(feature1, feature2, threshold):
        diff = np.subtract(feature1, feature2)
        dist = np.sum(np.square(diff), 1)
        print(dist)
        if dist < threshold:
            return True
        else:
            return False

    async def add_face(self, data):
        """
        :introduction 添加人脸到数据库
        """

        image = get_frame()

        # 保证照片中只有一张人脸
        faces = model.get(image)
        if len(faces) == 0:
            raise NoFaceError()
        if len(faces) > 1:
            raise MultiFaceError()

        # 提取人脸特征
        embedding = np.array(faces[0].embedding).reshape((1, -1))
        embedding = preprocessing.normalize(embedding)

        # 查询数据库中是否存在
        faces_in_db = await load_face()

        for db_face in faces_in_db:
            db_face_feature = np.frombuffer(db_face["face_img"], dtype=np.float32).reshape((1, -1))

            if self.feature_compare(embedding, db_face_feature, config.threshold):
                print("人脸已存在")

                return None

        # 保存到本地
        cv2.imencode('.png', image)[1].tofile(os.path.join(config.face_db, '%s.png' % data.username))

        # 添加到数据库
        face_feature = embedding.tobytes()

        user = User(username=data.username, org_id=data.orgId, face_img=face_feature)
        await user.save()

        return True

    async def recognition_face(self):
        """
        :introduction 人脸识别
        :returns
        """

        image = get_frame()
        # plt.imshow(image)
        # plt.axis('off')  # 隐藏坐标轴
        # plt.show()

        faces = model.get(image)

        faces_in_db = await load_face()

        for face in faces:
            result = dict()

            # 获取人脸属性
            result["bbox"] = np.array(face.bbox).astype(np.int32).tolist()
            if face.landmark is not None:
                result["landmark"] = np.array(face.landmark).astype(np.int32).tolist()

            # 开始人脸识别
            embedding = np.array(face.embedding).reshape((1, -1))
            embedding = preprocessing.normalize(embedding)

            result["user_id"] = 0
            result["username"] = "unknown"

            for db_face in faces_in_db:
                print(db_face)
                face_feature = np.frombuffer(db_face["face_image"], dtype=np.float32).reshape((1, -1))

                if self.feature_compare(embedding, face_feature, config.threshold):
                    print("已找到")
                    result["user_id"] = db_face["user_id"]
                    result["username"] = db_face["username"]
                else:
                    print("不匹配的人脸，请先注册！")

        return result

    async def delete_face(self, user_id):
        """
        :introduction 删除人脸
        """

        await User.filter(user_id=user_id).delete()

    # async def query_face(self):
    #     data = await User.all()
    #     return data

    # async def query_face_batch(self, data):
    #     # 开启摄像头
    #     cap = cv2.VideoCapture(0)
    #     ret, frame = cap.read()
    #     retval, b_data = cv2.imencode('.jpg', frame)
    #     # 关闭摄像头
    #     cap.release()
    #
    #     # image_data = data.imageByte.split(",")[-1]
    #     # b_data = base64.b64decode(image_data)
    #
    #     buffered = BytesIO(b_data)
    #     image = Image.open(buffered)
    #
    #     try:
    #         search_encoding = insight_face_utils.get_feature_data(image)
    #         results = []
    #
    #         for face in await User.all():
    #             encoding = np.frombuffer(face.face_img, dtype=np.float32)
    #             distance = np.linalg.norm(search_encoding - encoding)
    #             results.append((face.user_id, face.username, distance.item()))
    #
    #             print(f'distance to {face.username}: {distance}')
    #
    #         results.sort(key=lambda x: x[2])
    #
    #         if len(results) == 0:
    #             return []
    #         return results[0]
    #     except Exception as e:
    #         print(e)
    #
    #         return False
