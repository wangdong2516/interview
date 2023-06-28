import logging
import traceback

from django.http import Http404
from rest_framework.exceptions import ValidationError, MethodNotAllowed, APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler
from utils.error_code import *

api_logger = logging.getLogger("api")


def custom_exception_handler(exc, context):
    """
        DRF全局异常处理函数
    Args:
        exc: 错误类型
        context: 发生错误的上下文信息

    Returns:

    """

    response = exception_handler(exc, context)
    request = context["request"]

    if response is not None:

        if isinstance(exc, Http404):
            response.message = "页面未找到"
            response.code = PAGE_NOT_FOUND_ERROR  # noqa:F405
            response.data = []

        # 处理参数验证异常
        elif isinstance(exc, ValidationError):
            response.code = REQUEST_PARAMS_ERROR  # noqa:F405
            response.status_code = 200
            response.data = []
            response.message = exc.detail

        # 处理代码中手动抛出的异常
        elif isinstance(exc, APIException):
            response.code = exc.default_code
            response.message = exc.default_detail
            response.data.pop("detail")
            response.data = []
            response.status_code = exc.status_code

        # 处理方法不允许的异常
        elif isinstance(exc, MethodNotAllowed):
            response.code = METHOD_NOT_ALLOWED_ERROR  # noqa:F405
            response.message = "请求方式不允许"
            response.data = []

    # 代码中未捕获的异常处理
    else:
        response = Response(data={}, status=500)
        response.data["code"] = "500000"
        response.data["message"] = "INTERNAL SERVER ERROR"
        response.data["data"] = []

    data = response.data if response else {}

    request_data = (
        dict(request.query_params) if request.method == "GET" else request.data
    )

    api_logger.error(
        f"path:{request.path}, method:{request.method}, request_data:{request_data},"
        f"response_data:{data}, error:{traceback.format_exc()}"
    )

    return response


class InterviewAPIException(APIException):
    class CUSTOMER_INFO_NOT_EXISIS(APIException):
        """
        客户信息不存在
        """

        default_code = AUTHENTICATION_ERROR  # noqa:F405
        status_code = 200
        default_detail = "用户身份信息验证失败"
