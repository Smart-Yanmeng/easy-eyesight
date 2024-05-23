from service.user_service import UserService
from utils.glasses_detector_utils import has_glasses

state = {
    "code": 0,
    "msg": "wait face"
}

user = ""


def get_state():
    global user, state
    return state


def do_test_visual_acuity():
    # 扫描人脸
    results = UserService().recognition_face()
    print(results)

    # 眼镜识别
    if has_glasses():
        print("Glasses detection result: TRUE")
    else:
        print("Glasses detection result: FALSE")

    # 手势识别

    return
