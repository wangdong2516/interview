from typing import Any

from utils.status import StatusCodeEnum


class ReturnObj(object):

    def __init__(
            self, enum: StatusCodeEnum, success: bool, data: Any = None
    ):
        self.status_code = StatusCodeEnum.get_status_code(enum)
        self.message = StatusCodeEnum.get_message(enum)
        self.success = success
        self.data = data
