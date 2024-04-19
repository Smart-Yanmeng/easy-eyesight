from fastapi import APIRouter, HTTPException

from utils.glasses_detector_utils import has_glasses

glasses_api = APIRouter()


@glasses_api.get("/glasses")
async def judge_wear_glasses():
    try:
        if has_glasses():
            return {"code": 200, "message": "success", "data": True}
        else:
            return {"code": 200, "message": "success", "data": False}
    except:
        print("未识别到人脸！")

        raise HTTPException(status_code=400, detail="未识别到人脸")
