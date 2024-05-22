# import cv2
# import mediapipe as mp
# import math
# import glasses
# 
# mp_drawing = mp.solutions.drawing_utils
# mp_hands = mp.solutions.hands
# 
# mp_face_detection = mp.solutions.face_detection
# face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)
# 
# # 打开摄像头
# cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
# 
# # 设置手部检测参数
# hands = mp_hands.Hands(
#     max_num_hands=2,
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5
# )
# 
# # 循环读取摄像头数据
# # 检测人脸
# while True:
#     # 读取摄像头数据
#     ret, frame = cap.read()
# 
#     print("正在等待人脸")
#     if not ret:
#         print("Ignoring empty camera frame.")
#         continue
# 
#     # 将摄像头数据转换成RGB格式并进行手部检测
#     frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
# 
#     face_result = face_detection.process(frame)
# 
#     # 绘制检测结果并保存裁剪的人脸
#     if face_result.detections:
#         # 检测到有人脸
#         print("检测到人脸出现，正在向服务器确认身份：测试用户1")
# 
#         for detection in face_result.detections:
#             bboxC = detection.location_data.relative_bounding_box
#             # mp_drawing.draw_detection(frame, detection)
#             ih, iw, _ = frame.shape
#             x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
# 
#             try:
#                 flag = "has_glasses" if glasses.has_glasses(frame, detection) else "not"
#                 cv2.putText(frame, flag, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
#             except Exception as e:
#                 print(e)
#             # 在人脸周围绘制边界框
#             # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
# 
#     results = hands.process(frame)
# 
#     # 如果检测到手部，则获取手部位置和方向信息
#     if results.multi_hand_landmarks:
#         for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
#             # 绘制手部关键点
#             mp_drawing.draw_landmarks(
#                 frame,
#                 hand_landmarks,
#                 mp_hands.HAND_CONNECTIONS,
#                 mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
#                 mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2))
# 
#             # 获取手部方向信息
#             x_thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
#             y_thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
#             x_index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
#             y_index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
#             angle = math.atan2(y_thumb - y_index, x_thumb - x_index)
#             angle = math.degrees(angle)
# 
#             # 根据角度判断方向
#             if angle >= -45 and angle < 45:
#                 direction = "left"
#             elif angle >= 45 and angle < 135:
#                 direction = "up"
#             elif angle >= 135 or angle < -135:
#                 direction = "right"
#             else:
#                 direction = "down"
# 
#             # 获取手部类型信息
#             if results.multi_handedness[idx].classification[0].label == 'Left':
#                 hand = 'left'
#             else:
#                 hand = 'right'
# 
#             # 在图像上显示手部类型和方向
#             cv2.putText(frame, "h: " + hand + " d: " + direction,
#                         (int(x_thumb * frame.shape[1]), int(y_thumb * frame.shape[0])), cv2.FONT_HERSHEY_SIMPLEX, 1,
#                         (0, 255, 0), 2, cv2.LINE_AA)
# 
#     # 显示检测结果
# 
#     # frame = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
#     cv2.imshow('Gesture Detection', frame)
# 
#     # 等待用户按下ESC键退出程序
#     if cv2.waitKey(1) == 27:
#         break
# 
# # 释放资源
# cap.release()
# cv2.destroyAllWindows()
