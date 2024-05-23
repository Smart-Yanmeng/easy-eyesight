from fastapi import APIRouter

from pojo.po_models import Record
from pojo.vo_result import R
from service.record_service import *

record_api = APIRouter()


@record_api.get("")
async def getAllRecord():
    recorders = await Record.all()

    for record in recorders:
        print(record)

    return None


@record_api.post("/naked-eye")
async def doRecordWithNaked():
    if do_record_with_naked():
        return R.ok()

    return None


@record_api.post("/wear-glasses")
async def doRecordWithGlasses():
    if do_record_with_glasses():
        return R.ok()

    return None
