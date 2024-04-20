from utils.glasses_detector_utils import has_glasses

from costom_error import *


async def do_record_with_naked():
    if has_glasses():
        raise HasGlassesError()

    return True


async def do_record_with_glasses():
    if not has_glasses():
        raise NoGlassesError()

    return True
