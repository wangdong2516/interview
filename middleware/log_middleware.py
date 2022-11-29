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
        self.log = logging.getLogger('api_request')
        super(LogMiddleware, self).__init__(get_response)

    def get_parser_context(self, http_request):
        """
        Returns a dict that is passed through to Parser.parse(),
        as the `parser_context` keyword argument.
        """
        # Note: Additionally `request` and `encoding` will also be added
        #       to the context by the Request object.
        return {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {})
        }

    @staticmethod
    def get_parsers():
        """
        Instantiates and returns the list of parsers that this view can use.
        """
        return [parser() for parser in api_settings.DEFAULT_PARSER_CLASSES]

    @staticmethod
    def get_authenticators():
        """
        Instantiates and returns the list of authenticators that this view can use.
        """
        return [auth() for auth in api_settings.DEFAULT_AUTHENTICATION_CLASSES]

    def get_content_negotiator(self):
        """
        Instantiate and return the content negotiation class to use.
        """
        if not getattr(self, '_negotiator', None):
            self._negotiator = api_settings.DEFAULT_CONTENT_NEGOTIATION_CLASS()
        return self._negotiator

    def process_request(self, request):
        if not hasattr(self, 'start_time'):
            request_start_time = time.time()
            self.start_time = request_start_time

    def process_response(self, request, response):
        parser_context = self.get_parser_context(request)

        # 利用DRF封装的内容解析类(方法)来对请求的参数进行处理(转换成python内置类型)
        _request = Request(
            request,
            parsers=self.get_parsers(),
            authenticators=self.get_authenticators(),
            negotiator=self.get_content_negotiator(),
            parser_context=parser_context
        )

        self.log.info(
            f'cid:{request.correlation_id}, path:{_request.path}, method:{_request.method}, body:{_request.data},'
            f'query_params:{dict(_request.query_params)}, status_doe:{response.status_code},response:{response.data}'
        )

        if hasattr(self, 'start_time'):
            end_time = time.time()
            duration = end_time - self.start_time
            response.__setitem__("X-Page-Duration-ms", int(duration * 1000))
        return response

