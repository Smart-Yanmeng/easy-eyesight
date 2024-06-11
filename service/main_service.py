import math
import time

import cv2
import mediapipe as mp
from random import random

from service.user_service import UserService
from settings.face_model import FaceModel
from utils.capture_utils import get_frame
from utils.face_detector_utils import has_face
from utils.glasses_detector_utils import has_glasses

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

state = {
    "code": 0,
    "msg": "wait for user",
    "data": {}
}

user = {
    "user_id": -1,
    "user_name": ""
}

record = {
    "user": user,
    "left_with_glasses": 0.0,
    "right_with_glasses": 0.0,
    "left_naked_eye": 0.0,
    "right_naked_eye": 0.0,
    "create_time": 0.0
}

sight = 0.0
line_count = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
table = {
    0: "up",
    1: "down",
    2: "left",
    3: "right"
}


def get_state():
    global user, record, state
    return state


async def do_test_visual_acuity():
    global user, sight
    model = FaceModel.get_model()

    # 用户是否存在
    no_face_flag = 0
    # 是否是第一次测试
    detection_left = True
    # 是否佩戴眼镜
    is_wear_glasses = False

    # 扫描人脸，得到当前测试用户
    user_face = await UserService().recognition_face()
    print("user -> ", user_face)

    user["user_id"] = user_face["user_id"]
    user["user_name"] = user_face["username"]
    record["user"] = user
    record["create_time"] = time.time()

    # 眼镜识别，判断当前用户是否佩戴眼镜
    if has_glasses():
        is_wear_glasses = True

        print("Glasses detection result: TRUE")
    else:
        print("Glasses detection result: FALSE")

    # 手势识别
    while True:
        # 判断用户是否离开
        if not has_face():
            no_face_flag += 1

            if no_face_flag == 3:
                state["code"] = 200
                state["msg"] = "wait for user"
                print("无用户，进程结束！")

                return state

            time.sleep(2)
            continue
        no_face_flag = 0

        # 进入手势识别
        # do_test(detection_left)
        print(do_test(detection_left))

        time.sleep(10)

        # 手势识别结束，生成眼睛视力
        sight = 1.0

        # 测左眼：提示换眼睛
        if detection_left:
            # 戴眼镜
            if is_wear_glasses:
                record["left_with_glasses"] = sight
            # 不戴眼镜
            else:
                record["left_naked_eye"] = sight

            detection_left = False
            print("请换一只眼睛继续测量！")

            continue
        # 侧右眼：记录一次，若有戴眼镜，则询问是否需要进行裸眼测试
        else:
            # 戴眼镜
            if is_wear_glasses:
                record["right_with_glasses"] = sight

                print("测量结束，若佩戴眼镜，您可以摘下眼镜继续测量！")
                time.sleep(10)

                frame = get_frame()
                faces = model.get(frame)

                # 判断用户是否离开或依然戴着眼镜
                if not faces or has_glasses():
                    state["code"] = 200
                    state["msg"] = "record successful"
                    state["data"] = record
                    print("您的视力测试已完成，正在生成报告...")

                    return state

                detection_left = True
                is_wear_glasses = False

                continue
            # 不戴眼镜
            else:
                record["right_naked_eye"] = sight

                state["code"] = 200
                state["msg"] = "record successful"
                state["data"] = record
                print("您的视力测试已完成，正在生成报告...")

        return state


def do_test(is_left):
    now, hand = ("左", "右") if is_left else ("右", "左")
    print(f"请用{now}手握住挡眼板遮住{hand}眼进行测试！")

    time.sleep(5)

    return "good"
    # while True:
    #     time.sleep(1)


def test_aline(line, eye):
    global msg
    # 每个等级根据对应数量条件进行测试
    last_flag = False

    for i in range(1, line_count[line - 1] + 1):
        is_right = test_one(line, eye)

        if is_right:
            if last_flag:
                # 连对两个，这行通过
                return True
            else:
                last_flag = True
        else:
            # 若五秒内没做出正确手势，即直接判断不通过，不能因为要考虑到个别不必要的容错而降低系统的整体效率
            return False


def test_one(level, eye):
    global last_flag, edata, data, msg

    is_right = False

    # 生成对应行的 E 字数据：大小和方向
    random_number = random.randint(0, 3)
    while True:
        if random_number == last_flag:
            random_number = random.randint(0, 3)
        else:
            last_flag = random_number

            break

    edata["position"] = table[random_number]
    edata["size"] = level

    time.sleep(2)

    # 最大五秒
    start_time = time.time()

    while True:
        print(start_time)
        if time.time() - start_time > 5:
            break
        frame = get_frame()
        hand_data = get_direction(frame)

        if (hand_data == False):
            msg, data = "未检测到手势", []
            continue
        else:
            # 识别到手势
            msg = "请根据上图内容做出对应手势并保持两秒以上"
            data, frame = hand_data[0], hand_data[1]
            d = [i for i in data if i[1] == eye]
            # 如果手不存在，继续检测
            if (len(d) == 0):
                hand = "右" if eye == "right" else "左"
                msg, data = "请使用" + hand + "手做出手势！", []
                continue
            else:
                if (d[0][0] == edata['position']):
                    is_right = True
                    break
    return is_right


def get_direction(frame):
    results = hands.process(frame)
    # print(results.multi_hand_landmarks)
    # 如果检测到手部，则获取手部位置和方向信息

    if results.multi_hand_landmarks:
        data = []
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # 绘制手部关键点
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2))

            # 获取手部方向信息
            x_thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
            y_thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
            x_index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
            y_index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            angle = math.atan2(y_thumb - y_index, x_thumb - x_index)
            angle = math.degrees(angle)

            # 根据角度判断方向
            if angle >= -45 and angle < 45:
                direction = "left"
            elif angle >= 45 and angle < 135:
                direction = "up"
            elif angle >= 135 or angle < -135:
                direction = "right"
            else:
                direction = "down"

            # 获取手部类型信息
            if results.multi_handedness[idx].classification[0].label == 'Left':
                hand = 'left'
            else:
                hand = 'right'

            data.append([direction, hand])
            # 在图像上显示手部类型和方向
            cv2.putText(frame, "h: " + hand + " d: " + direction,
                        (int(x_thumb * frame.shape[1]), int(y_thumb * frame.shape[0])), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2, cv2.LINE_AA)

        return data, frame

    return False
