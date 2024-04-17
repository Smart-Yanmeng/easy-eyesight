from fastapi import APIRouter, HTTPException

from pojo.dto_models import FaceImgDto
from pojo.po_models import User
from service.user_service import UserService, load_face

user_api = APIRouter()


@user_api.get("/")
async def getAllUser():
    users = await User.all()

    for user in users:
        print(user.user_id, user.username)

    return None


@user_api.post("/user/face")
async def insert_user(request: FaceImgDto):
    if await UserService().add_face(request):
        return {"code": 0, "message": "success"}

    raise HTTPException(status_code=400, detail="未识别到人脸")


@user_api.delete("/user/face")
async def delete_user(request: int):
    if await UserService().delete_face(request):
        return {"code": 0, "message": "success"}

    raise HTTPException(status_code=400, detail="系统出错")


@user_api.get("/user/face")
async def query_user():
    data = await load_face()

    for datum in data:
        print("user_id: ", datum.user_id)
        print("username: ", datum.username)
        print("username: ", datum.face_img)

    return {"code": 0, "message": "success"}


@user_api.post("/user/face/recognize")
async def recognize_face():
    data = await UserService().recognituon_face()
    if data:
        return {"code": 0, "message": "success", "data": data}

    raise HTTPException(status_code=400, detail="未识别到人脸")
