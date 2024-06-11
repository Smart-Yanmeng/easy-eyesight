from service.user_service import model
from utils.capture_utils import get_frame


def has_face():
    frame = get_frame()
    faces = model.get(frame)

    if not faces:
        return False
    return True


if __name__ == '__main__':
    has_face()
