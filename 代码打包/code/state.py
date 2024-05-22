import cv2
import mediapipe as mp
import math
import glasses_detector as glasses
import time
import threading
import random

from face_service import *

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)

cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
# hands:[{"hand":"left","direction":"up"},{"hand":"right","direction":"up"}]

user, state, msg, data, edata = "", "", "", [], {}

table = {0: "up", 1: "down", 2: "left", 3: "right"}

# condtion = [1,1,1,2,2,3,3,3,4,4,4]

condtion = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

# line_count = [2,2,2,3,3,4,4,5,6,7,8]

line_count = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]

stage_data = [[0, 2], [3, 7], [8, 10]]

test_result = []

last_user = "no_user"

last_flag = 0

is_glasses = False

face_service = Face_service()

# sound = "";

# 设置手部检测参数
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


def get_frame():
    ret, frame = cap.read()
    frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    # frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    return frame


def get_face_area(frame):
    # global sound
    cv2.imwrite("temp.png", frame)
    face_result = face_detection.process(frame)

    if face_result.detections:
        for detection in face_result.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
            # 识别出的人脸区域图像
            cropped_face = frame[y:y + h, x:x + w]

            # 模拟人脸识别任务
            user = face_service.search_face_line(cropped_face)
            if (user == False):
                # sound = "rescan"
                return "正在重新扫描人脸，请面向摄像头"

            if (user == []):
                # sound = "nouser"
                return "当前用户不存在或未注册！"

            # user = user[1]

            # user = "测试用户1"
            # print("识别成功："+user)
            # print("人脸识别成功，人脸置信度："+str(detection.score[0]))

            try:
                flag_glasses = glasses.has_glasses("temp.png")
                if (flag_glasses == -1):
                    # sound = "rescan"
                    return "正在重新扫描人脸，请面向摄像头"
                # flag = "has_glasses " if glasses.has_glasses(cropped_face) else "not "
                # cv2.putText(frame, flag+str(detection.score[0]), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                return (cropped_face, flag_glasses, user)
            except Exception as e:
                print(e)
    return "未检测到人脸"


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


def start():
    global state, msg, data, edata, user, last_user
        # , sound
    # 循环读取摄像头数据并写入全局变量

    no_face = True

    last_user = "no_user"

    while True:
        # 读取摄像头数据
        frame = get_frame()

        state = "待检测状态，正在等待测试者人脸"
        msg = "正在等待,请正视摄像头"
        # sound = "wait_face"

        # has_glasses = False

        if (no_face):
            user = "未识别"
            face_data = get_face_area(frame)

            if (isinstance(face_data, tuple) == False):
                msg = face_data
                time.sleep(2)
                continue
            else:
                user = face_data[2]
                face_data, has_glasses = face_data[0], face_data[1]
                print(user)

                print("glasses:" + str(has_glasses))

                # 如果这个用户第一次测试
                if (user != last_user):

                    # 戴眼镜，提示摘掉
                    if (has_glasses == True):
                        is_glasses = True
                        msg = "请先摘下眼镜进行裸眼视力测试！"
                        # sound = "takeoff"
                        time.sleep(3)
                        continue
                else:
                    # 戴眼镜二次矫正测试
                    if (has_glasses == False):
                        msg = "若有佩戴眼镜，请戴上眼镜进行矫正视力测试！否则请离开！"
                        # sound = "over"
                        time.sleep(3)
                        continue

                    if (len(test_result) == 4):
                        # 已经测过两次了，提示离开
                        msg = "您的视力测试已完成，请离开"
                        # sound = "over"
                        time.sleep(5)
                        continue

                no_face = False
                msg = "人脸识别成功：测试用户1"
                state = "正在进行手势识别"
        else:
            # 手势识别阶段
            test_data = test_round()
            last_user = user
            # print(test_data)

            # 测完一轮，重置标签
            no_face = True
            if (has_glasses):
                msg = "测试结束，" + last_user + ",你的数据：" + todata(test_result) + "，您的视力测试已完成，请离开"
                # sound = "over"
            else:
                msg = "测试结束，" + last_user + ",你的数据：" + todata(
                    test_result) + "，若有佩戴眼镜，请戴上眼镜后继续进行矫正视力测试。否则请离开测试区域"
                # sound = "over_part"
            # print(no_face, has_glasses)

            time.sleep(10)


# 两眼一轮，不管裸眼还是矫正
def test_round():
    global state, msg, data, edata, last_user, test_result\
        # , sound
    # 手势识别阶段
    # 先测右眼
    eye = "right"

    # 清空当前测试数据
    if (len(test_result) == 4):
        test_result = []
    while True:
        size = 0
        now, hand = ("左", "右") if (eye == "right") else ("右", "左")
        # 检测到人脸之后给用户三秒钟时间调整姿态
        msg = "请" + now + "手握住挡眼板挡遮住" + now + "眼进行下一步测试"
        # sound = eye

        time.sleep(1)
        over = False
        last_flag = 0
        # 共测试11个等级0-10
        stage = get_stage(eye)
        if (stage == None):
            # 视力1.0，不用再测了
            vision = 10
        else:
            vision = 0
            for i in range(stage[0], stage[1]):
                if (test_aline(i, eye) == False):
                    vision = i - 1
                    break
                else:
                    vision = i

        test_result.append(vision)
        eye = "left" if eye == "right" else "over"
        if (eye == "over"):
            break

    return test_result


def get_stage(eye):
    for a in stage_data:
        is_pass = test_aline(a[1], eye)
        if (is_pass == False):
            return a
    return None


def test_aline(line, eye):
    global msg
    # right,fail = 0,0
    # 每个等级根据对应数量条件进行测试
    last_flag = False
    for i in range(1, line_count[line - 1] + 1):
        # print("等级："+str(i)+" 次数："+str(j)+"，最多次数："+str(line_count[i]))
        is_right = test_one(line, eye)
        if (is_right):
            if (last_flag == True):
                # 连对两个，这行通过
                return True
            else:
                last_flag = True
        else:
            # 错了就是错了，这里不考虑容错，容错在单个测试的五秒内已经给足时间
            # 若五秒内没做出正确手势，即直接判断不通过，不能因为要考虑到个别不必要的容错而降低系统的整体效率
            return False

        # 如果正确或错误过半则退出当前行的测试
        # if(fail == condtion[i] or right == condtion[i]):
        #    print(fail,right,condtion[i])
        #    break


def test_one(level, eye):
    global last_flag, edata, data, msg

    # 生成对应行的E字数据：大小和方向
    random_number = random.randint(0, 3)
    while (True):
        if (random_number == last_flag):
            random_number = random.randint(0, 3)
        else:
            last_flag = random_number
            break

    edata['position'] = table[random_number]
    edata['size'] = level

    time.sleep(2)

    is_right = False

    # 最大五秒
    start_time = time.time()

    while True:
        # print(time.time())
        print(start_time)
        if (time.time() - start_time > 5):
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


def get_state():
    global user, state, msg, data, edata\
        # , sound

    result = {
        'user': user,
        'state': state,
        'msg': msg,
        'data': data,
        'edata': edata,
        # 'sound': sound
    }

    return result


def todata(data):
    table = [0.0, 0.1, 0.12, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]

    data = [0 if (i == -1) else i + 1 for i in data]

    data[0], data[1] = table[data[0]], table[data[1]]
    if (len(data) == 4):
        data[2], data[3] = table[data[2]], table[data[3]]
        return "裸眼：右" + str(data[0]) + "，左" + str(data[1]) + "；矫正：右" + str(data[2]) + "，左" + str(data[3])
    else:
        return "裸眼：右" + str(data[0]) + "，左" + str(data[1])


t1 = threading.Thread(target=start)
t1.start()
print("线程已启动，开始读取线程状态")
# time.sleep(5)
# while True:
# time.sleep(1)
# print("读取信息")
# print(get_state())
