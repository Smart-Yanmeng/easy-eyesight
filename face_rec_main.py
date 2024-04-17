import cv2

from service.user_service import UserService
from utils.insight_face_utils import FaceRecognition
import numpy as np


def capture_image():
    # 打开摄像头
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("无法打开摄像头。")
        return None

    # 捕获图像
    ret, frame = cap.read()

    if not ret:
        print("无法捕获图像。")
        return None

    # 关闭摄像头
    cap.release()

    return frame


if __name__ == '__main__':
    image = capture_image()

    if image is not None:
        print("图像成功捕获。")
        print("图像类型:", type(image))
        print("图像形状:", image.shape)
    else:
        print("未能捕获图像。")
    # img = cv2.imread("Zhou_Jielun.jpg")
    print(type(image))

    face_recognition = FaceRecognition("settings/config.yaml")
    user_id = face_recognition.register(image)

    print("user_id: ", user_id)

# if __name__ == '__main__':
    # img = cv2.imread("Cheng_Long.jpg")
    # image = capture_image()
    #
    # face_recognition = FaceRecognition("settings/config.yaml")
    # result = face_recognition.recognition(image)
    # print(result)
