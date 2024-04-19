import cv2


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

    if frame is not None:
        print("图像成功捕获")
        print("图像类型: ", type(frame))
        print("图像形状: ", frame.shape)
    else:
        print("未能捕获图像")

        return None
    return frame
