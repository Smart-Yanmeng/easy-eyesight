from fastapi import APIRouter, HTTPException

from costom_error import NoFaceError
from utils.glasses_detector_utils import has_glasses

glasses_api = APIRouter()


@glasses_api.get("")
async def judge_wear_glasses():
    try:
        if has_glasses():
            return {"code": 200, "message": "success", "data": True}
        else:
            return {"code": 200, "message": "success", "data": False}
    except:
        error = NoFaceError()

        raise HTTPException(status_code=400, detail=error.message)
