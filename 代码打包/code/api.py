import uvicorn
from io import BytesIO
import sys
import base64
import requests
import datetime
import state
from PIL import Image

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from face_service import *

import time

# 创建框架
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# 允许跨域AJAX请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_stats")
def get_stats():
    return state.get_state()


face_service = Face_service()


# 定义请求体参数模型
class ImageRequest(BaseModel):
    image: str
    username: str = ""


# 人脸录入接口
@app.post("/api/face/add")
def add_face(request: ImageRequest):
    # 从请求中获取base64编码的图片数据
    image_data = request.image.split(",")[-1]
    b_data = base64.b64decode(image_data)
    with open("static/" + request.username + ".jpg", 'wb') as file:
        file.write(b_data)
    image = Image.open(BytesIO(b_data))

    flag = face_service.add_face(image, request.username)
    if (flag == False):
        raise HTTPException(status_code=400, detail="未识别到人脸")
    # 人脸添加成功
    return {"code": 0, "message": "success"}


# 人脸识别接口
@app.post("/api/face/recognize")
def recognize_face(request: ImageRequest):
    # 从请求中获取base64编码的图片数据
    image_data = request.image.split(",")[-1]
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    data = face_service.search_face_line(image)

    if (data == False):
        raise HTTPException(status_code=400, detail="该人脸数据不存在！")

    return {"code": 0, "message": "success", "username": data[1]}


@app.get("/api/faces")
def get_all():
    # 获取全部人脸数据
    data = face_service.get_faces()
    print(data)
    return {"code": 0, "message": "success", "data": data}


@app.delete("/api/faces/{id}")
def delete_face(id: str):
    face_service.delete_face_by_id(id)
    return {"code": 0, "message": "success"}


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=9999)
