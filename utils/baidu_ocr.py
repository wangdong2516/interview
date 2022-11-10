from pathlib import Path
from typing import Union

from aip import AipOcr
from settings.base_settings import APP_ID, API_KEY, OCR_SECRET_KEY
from utils.status import StatusCodeEnum


class OCRUtil(object):

    def __init__(self):
        self.ocr_client = self.create_client()

    @staticmethod
    def create_client() -> AipOcr:
        return AipOcr(APP_ID, API_KEY, OCR_SECRET_KEY)

    def accurate_image_word(self, image_file_path: str = '', content: bytes = b''):
        """
            高精度带位置的文字识别
        Args:
            image_file_path:
            content: 图片二进制内容

        Returns:

        """
        path = Path(image_file_path)
        if not path.exists():
            return StatusCodeEnum.FILE_PATH_NOT_EXISTS.value
        if not content:
            if not image_file_path:
                raise ValueError('you must provide image_file_path if not content params')
            with open(image_file_path, 'rb') as f:
                content = f.read()
        if not isinstance(content, bytes):
            raise ValueError('content must be the instance of bytes')
        res_image = self.ocr_client.accurate(content)
        # 当识别到的文字数量小于等于1的时候，重新进行识别
        while res_image.get('words_result_num', 0) <= 1:
            options = {'recognize_granularity': "small"}
            res_image = self.ocr_client.accurate(content, options=options)
        return res_image


if __name__ == '__main__':
    ocr_util = OCRUtil()
    res = ocr_util.accurate_image_word('../41d77151526165ca03de7d1ce0f60fea.jpg')
    print(res)
