import cv2
import numpy as np
import dlib
from PIL import Image

from utils.capture_utils import capture_image

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')


def has_glasses():
    # try:
    img = capture_image()

    # img = dlib.load_rgb_image(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    try:
        faces = detector(img)
        if len(faces) != 1:
            print("识别到多个人脸")

            raise Exception("多个人脸")
        rect = faces[0]
        sp = predictor(img, rect)
        landmarks = np.array([[p.x, p.y] for p in sp.parts()])
        print(landmarks)
    except:
        print("未识别到人脸")

        return -1

    nose_bridge_x = []
    nose_bridge_y = []

    for i in [28, 29, 30, 31, 33, 34, 35]:
        nose_bridge_x.append(landmarks[i][0])
        nose_bridge_y.append(landmarks[i][1])

    # x_min and x_max
    x_min = min(nose_bridge_x)
    x_max = max(nose_bridge_x)

    # ymin (from top eyebrow coordinate),  ymax
    y_min = landmarks[20][1]
    y_max = landmarks[31][1]

    # img2 = Image.open(path)
    img2 = Image.fromarray(img)

    img2 = img2.crop((x_min, y_min, x_max * 0.99, y_max * 0.95))

    # 高斯滤波
    img_blur = cv2.GaussianBlur(np.array(img2), (3, 3), sigmaX=0, sigmaY=0)

    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
    edges_center = edges.T[(int(len(edges.T) / 2))]

    if 255 in edges_center:
        print("戴了眼镜")
        return True
    else:
        print("未带眼镜")
        return False


if __name__ == '__main__':
    has_glasses()
