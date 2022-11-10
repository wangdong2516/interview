from pathlib import Path
from typing import Union

from utils.status import StatusCodeEnum
from utils.return_obj import ReturnObj


class FileUtil:
    """
        文件处理工具类
    """

    @staticmethod
    def make_dir_if_not_exists(folder_path: Union[str, Path]) -> bool:
        """
             当目录不存在的时候创建目录
        Args:
            folder_path: 目录路径

        Returns:
            True: 创建目录成功
            False:创建目录失败
        """

        if isinstance(folder_path, str):
            folder_path = Path(folder_path)
        if not isinstance(folder_path, Path):
            raise ValueError('folder path must be one of the instance of [str, pathlib.Path]')
        try:
            # 创建目录，当目录已经存在的时候不报错
            folder_path.mkdir(exist_ok=True)
            return True
        except (FileNotFoundError, OSError) as error:
            return False

    def save_file(self, file_path: Union[Path, str], content: Union[bytes, str]) -> ReturnObj:
        """
            写入文件，当文件所在父目录不存在的时候进行创建
        Args:
            file_path:文件完整路径
            content: 文件内容

        Returns:
            ReturnObj
        """
        if isinstance(file_path, str):
            file_path = Path(file_path)
        if not isinstance(file_path, Path):
            raise ValueError('folder path must be one of the instance of [str, pathlib.Path]')
        if not file_path.parent.exists():
            dir_create_result = self.make_dir_if_not_exists(file_path.parent)
            if not dir_create_result:
                return ReturnObj(success=False, enum=StatusCodeEnum.MAKE_DIR_FAILED)
        if isinstance(content, str):
            content = content.encode('utf-8')
        try:
            with open(str(file_path), 'wb') as f:
                f.write(content)
            return ReturnObj(success=True, enum=StatusCodeEnum.OK)
        except Exception as e:
            return ReturnObj(success=False, enum=StatusCodeEnum.WRITE_FILE_FAILED)

    @staticmethod
    def read_file(file_path: str) -> bytes:
        """
            一次性读取文件内容
        Args:
            file_path: 文件路径

        Returns:
            文件内容二进制
        """
        content = b''
        with open(file_path, 'rb') as f:
            content = f.read()
        return content
