from enum import Enum


class StatusCodeEnum(Enum):
    """
        状态码枚举类
    """

    OK = (00000, 'success')
    ERROR = (40000, '错误')
    REQUEST_ERROR = (40001, '请求第三方服务出现错误，请求失败')
    SERVER_ERR = (50000, '服务器异常')
    FILE_PATH_NOT_EXISTS = (50001, '文件不存在')
    MAKE_DIR_FAILED = (50002, '创建目录失败')
    WRITE_FILE_FAILED = (50003, '写入文件失败')

    @classmethod
    def get_status_code(cls, attribute):
        return attribute.value[0]

    @classmethod
    def get_message(cls, attribute):
        return attribute.value[1]
