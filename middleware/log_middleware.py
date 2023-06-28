import json
import logging
import time

from django.utils.deprecation import MiddlewareMixin
from rest_framework.request import Request
from rest_framework.settings import api_settings


class LogMiddleware(MiddlewareMixin):
    """
    日志处理中间件
    """

    def __init__(self, get_response):
        """
            初始化方法，添加记录请求的日志
        Args:
            get_response: 视图函数类中的请求方式对应的方法
        """
        self.log = logging.getLogger("api_request")
        super(LogMiddleware, self).__init__(get_response)

    def __call__(self, request):
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            data = json.loads(request.body) if request.body else {}
        elif request.method == "GET":
            data = dict(request.GET)
        else:
            data = {}
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time
        response["X-Page-Duration-ms"] = int(duration * 1000)

        # 代码中可以捕获的异常
        if getattr(response, "data", None):
            response_body = response.data
        else:
            response_body = {}

        self.log.info(
            f"path:{request.path}, method:{request.method}, user:{request.user}, request_data:{data},"
            f"response_data:{response_body} duration:{duration}s"
        )

        if hasattr(self, "start_time"):
            end_time = time.time()
            duration = end_time - self.start_time
            response.__setitem__("X-Page-Duration-ms", int(duration * 1000))
        return response
