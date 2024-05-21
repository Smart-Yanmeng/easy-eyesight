import cv2
import mediapipe as mp
import os

# 初始化MediaPipe Face Detection组件
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)

output_dir = "detected_faces"
os.makedirs(output_dir, exist_ok=True)

def save_cropped_face(image, detection, count):
    h, w, _ = image.shape
    bboxC = detection.location_data.relative_bounding_box
    x, y, width, height = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)

    # 裁剪人脸并保存
    cropped_face = image[y:y+height, x:x+width]
    save_path = os.path.join(output_dir, f"face_{count}.jpg")
    try:
        cv2.imwrite(save_path, cropped_face)
    except Exception as e:
        print(e)

def main():
    # 打开摄像头
    cap = cv2.VideoCapture(0)
    face_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 转换图像格式
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 进行人脸检测
        result = face_detection.process(frame_rgb)

        # 绘制检测结果并保存裁剪的人脸
        if result.detections:
            for detection in result.detections:
                mp_drawing.draw_detection(frame, detection)
                #save_cropped_face(frame, detection, face_count)
                face_count += 1

        # 显示检测结果
        cv2.imshow('Face Detection', frame)

        # 按下 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
