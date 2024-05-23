from fastapi import APIRouter

from service.main_service import do_test_visual_acuity

process_api = APIRouter()


@process_api.get('/do-process')
async def do_process():
    """
    :introduce 整体流程
    """
    do_test_visual_acuity()

    return None
