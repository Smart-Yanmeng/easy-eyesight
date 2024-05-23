from fastapi import APIRouter, HTTPException

from pojo.dto_models import FaceImgDto
from pojo.po_models import User
from pojo.vo_result import R
from service.user_service import UserService, load_face

user_api = APIRouter()


@user_api.get("")
async def getAllUser():
    users = await User.all()

    userDict = {}
    for user in users:
        userDict[user.user_id] = user.username
        print(user.user_id, user.username)

    return userDict


@user_api.post("/face")
async def insert_user(request: FaceImgDto):
    if await UserService().add_face(request):
        return R.ok()

    raise HTTPException(status_code=400, detail="未识别到人脸")


@user_api.delete("/face")
async def delete_user(request: int):
    if await UserService().delete_face(request):
        return R.ok()

    raise HTTPException(status_code=400, detail="系统出错")


@user_api.get("/face")
async def query_user():
    data = await load_face()

    for datum in data:
        datum.face_img = str(datum.face_img)

    return R.ok(data=data)


@user_api.post("/face/recognize")
async def recognize_face():
    data = await UserService().recognition_face()
    if data:
        return R.ok(data=data)

    raise HTTPException(status_code=400, detail="未识别到人脸")
