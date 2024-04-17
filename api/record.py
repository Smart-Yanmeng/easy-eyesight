from fastapi import APIRouter

from pojo.po_models import Record

record_api = APIRouter()


@record_api.get("/record")
async def getAllRecord():
    recorders = await Record.all()

    for record in recorders:
        print(record)

    return None
