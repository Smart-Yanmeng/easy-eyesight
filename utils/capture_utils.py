import cv2

cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)


########
# TEST #
########
def capture_image():
    # 打开摄像头
    cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("无法打开摄像头")

        return None

    # 捕获图像
    ret, frame = cap.read()
    if not ret:
        print("无法捕获图像")

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


###########
# OPENING #
###########
def get_frame():
    ret, frame = cap.read()
    if not ret:
        print("无法捕获图像")

        return None

    if frame is not None:
        print("图像成功捕获")
        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    else:
        print("未能捕获图像")

        return None
    return frame
