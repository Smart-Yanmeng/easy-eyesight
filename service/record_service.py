from utils.glasses_detector_utils import has_glasses

from costom_error import *


async def do_record_with_naked():
    """
    :introduction: 裸眼测试
    """
    if has_glasses():
        raise HasGlassesError()

    return True


async def do_record_with_glasses():
    """
    :introduction: 戴镜测试
    """
    if not has_glasses():
        raise NoGlassesError()

    return True
