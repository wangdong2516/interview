import logging
from django.utils.deprecation import MiddlewareMixin


class LogMiddleware(MiddlewareMixin):
    """
        日志处理中间件
    """

    def __init__(self, get_response):
        """
            初始化方法，添加记录请求的日志
        Args:
            get_response:
        """
        self.log = logging.getLogger('api_request')
        super(LogMiddleware, self).__init__(get_response)

    def __call__(self, request, *args, **kwargs):
        """
            在实例化的时候调用
        Args:
            *args:
            **kwargs:

        Returns:

        """
        print('被掉用了')
        return super(LogMiddleware, self).__call__(request)




