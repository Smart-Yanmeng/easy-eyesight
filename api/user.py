import base64

from fastapi import APIRouter

from pojo.dto_models import ImageRequestDto
from pojo.po_models import *

user_api = APIRouter()


@user_api.get("/")
async def getAllUser():
    users = await User.all()

    for user in users:
        print(user.user_id, user.username)

    return None


@user_api.post("/user/face/add")
def insert_user(request: ImageRequestDto):
    image_data = request.imageByte.split(",")[-1]
    image_bin_data = base64.b64decode(image_data)
