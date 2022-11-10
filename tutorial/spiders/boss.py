import time
from typing import List, Dict

import scrapy
import re

from PIL import Image
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.common.by import By
import httpx
from selenium.webdriver import ActionChains
from utils.baidu_ocr import OCRUtil
from utils.file_util import FileUtil
from utils.return_obj import ReturnObj
from utils.status import StatusCodeEnum


class BossSpider(scrapy.Spider):

    # 爬虫的名称，每个爬虫必须有唯一的名称，不能重复也不能和其他的爬虫名称相同
    name = "boss"
    start_urls = [
        'https://www.zhipin.com/'
    ]

    def __init__(self, *args, **kwargs):
        self.browser = None
        super(BossSpider, self).__init__(*args, **kwargs)

    @staticmethod
    def create_webdriver(executable_path: str) -> webdriver.Chrome:
        """
            创建浏览器驱动
        Args:
            executable_path: 浏览器驱动的可执行路径

        Returns:

        """
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options, executable_path=executable_path)
        return driver

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url)

    @staticmethod
    def extract_verify_image_src(content: str) -> str:
        """
            提取图片的链接地址
        Args:
            content: 图片验证码标签文本数据

        Returns:

        """
        image_src = re.search(r'\(.*\)', content)
        if image_src:
            return re.sub(r'[() "]', '', image_src.group())
        return ''

    @staticmethod
    def download_with_retry(url: str, retry: int = 1) -> httpx.Response:
        """
            向指定的url发送get请求
        Args:
            url: url
            retry: 重试次数(不成功的情况下进行重试)

        Returns:

        """
        response = httpx.get(url=url, timeout=5)
        if not response.status_code == 200:
            # 请求失败之后进行重试
            retry_num = 0
            while retry_num <= retry:
                response = httpx.get(url=url, timeout=5)
                if not response.status_code == 200:
                    retry_num += 1
                else:
                    break

        return response

    @staticmethod
    def change_image_light(image_path: str, changed_image_path: str = ''):
        """
            对图像进行二值化，改变图像的颜色，并且保存改变之后的图片
            可以选择将源图片进行覆盖，也可以选择另存为新的图片
        Args:
            image_path: 图片路径
            changed_image_path: 将图片二值化之后保存的路径，默认为空

        Returns:

        """

        img = Image.open(image_path)
        image = img.convert('L')
        pixels = image.load()
        for x in range(image.width):
            for y in range(image.height):
                if pixels[x, y] > 150:
                    pixels[x, y] = 255
                else:
                    pixels[x, y] = 0
        image.save(changed_image_path)

    def image_ocr(self, verify_image_src: str, directory: str):
        """
            下载图像，调用百度OCR识别(高精度带位置)识别并且保存图片到指定的目录中
        Args:
            verify_image_src: 图片路径
            directory: 图片存储目录

        Returns:

        """
        response = self.download_with_retry(verify_image_src)
        if not response.status_code == 200:
            return ReturnObj(success=False, enum=StatusCodeEnum.REQUEST_ERROR)

        # 拿到图片的数据
        image_bytes = response.content
        # 图片文件名后缀
        image_suffix = re.sub(r'\?.*', '', verify_image_src.split('.')[-1])
        # 图片文件名前缀
        image_prefix = re.search(r'=(.*)', verify_image_src).groups()[0] if re.search(r'=(.*)', verify_image_src).groups()[0] else f'unknown{time.ctime()}'
        # 保存图片
        file_util = FileUtil()
        image_path = f'{directory}/{image_prefix}.{image_suffix}'
        changed_image_path = f'{directory}/{image_prefix}_2.{image_suffix}'
        ret_value = file_util.save_file(image_path, image_bytes)
        if not ret_value.success:
            return ret_value
        # 将图片进行二值化处理
        self.change_image_light(image_path=image_path, changed_image_path=changed_image_path)
        file_path = changed_image_path if changed_image_path != image_path else image_path
        image_bytes_changed = file_util.read_file(file_path=file_path)

        ocr_util = OCRUtil()
        res = ocr_util.accurate_image_word(content=image_bytes_changed)
        return res

    @staticmethod
    def click_words(words_position_info: List[Dict], browser: webdriver.Chrome):
        """
            依次点击图片中的文字
        Args:
            words_position_info: 文字位置信息
            browser: 浏览器对象

        Returns:

        """
        image = browser.find_element(by=By.XPATH, value='//div[@class="geetest_item_wrap"]')
        for info in words_position_info:
            ActionChains(browser).move_to_element_with_offset(
                to_element=image, xoffset=info['location']['left'] + 20,
                yoffset=info['location']['top'] + 20
            ).click().perform()
            print('ssssssss')

    def handle_verify_image_ocr(self, verify_image_src: str, browser: webdriver.Chrome):
        """
            处理图片验证码图片文字识别
        Args:
            verify_image_src: 图片验证码(大图)url
            browser: 浏览器对象

        Returns:

        """

        # 大图片文字的识别结果
        image_ocr_res = self.image_ocr(verify_image_src, self.settings['VERIFY_IMAGE_BIG_DIR'])
        print(f'获取到百度OCR的识别结果:{image_ocr_res}')
        if image_ocr_res.get('words_result'):
            print(f'开始点击图片中的文字')
            self.click_words(image_ocr_res['words_result'], browser=browser)

    def verify_code_login(self, login_url: str):
        # 创建一个浏览器驱动
        browser = self.create_webdriver(self.settings['SELENIUM_DRIVER_EXECUTABLE_PATH'])
        # 使用浏览器加载登录页面
        browser.get(url=login_url)
        # 定位验证码登录的按钮位置
        browser.find_element(by=By.XPATH, value='//a[@class="pwd-login-btn"]').click()
        # 定位手机号输入框的位置
        browser.find_element(by=By.XPATH, value='//input[@name="phone"]').send_keys(18734872516)
        # 定位点击按钮进行验证位置
        browser.find_element(by=By.XPATH, value='//div[contains(@id, "verrify")]').click()
        # 隐式等待，最多等待20秒
        browser.implicitly_wait(5)

        # 验证图片的地址
        verify_image_src = ''
        try:
            slipper_background_image = browser.find_element(by=By.XPATH, value='//img[@class="yidun_bg-img"]')
            verify_image_src = slipper_background_image.get_attribute('src')
            print(verify_image_src)
        except Exception as e:
            print('不是滑块验证方式')

        try:
            time.sleep(10)
            # browser.find_element(by=By.XPATH, value='//div[@class="verify-init-btn"]').click()
            # print('点击成功')
            browser.find_element(by=By.XPATH, value='//div[@class="yidun_intelli-tips"]').click()
            print('点击成功2')
        except Exception as e:
            print(e)
            print('不是点击验证方式')

        # try:
        #     # 大图的图片地址
        #     background_image = browser.find_element(by=By.XPATH, value='//div[@class="geetest_item_wrap"]')
        #     content = background_image.get_attribute('style')
        #     verify_image_src_big = self.extract_verify_image_src(content)
        #     self.handle_verify_image_ocr(verify_image_src_big, browser=browser)
        # except Exception as e:
        #     print(e)
        #     print('不是图形验证码验证方式')

        # browser.find_element(by=By.XPATH, value='//button[@class="btn btn-sms"]').click()

    def parse(self, response, **kwargs):
        """
            在生成response请求之后处理(调用)
        """
        # 提取boss页面的登录链接
        login_url = response.xpath('//a[@ka="header-login"]/@href').extract()[0]
        # 使用验证码方式登录boss
        self.verify_code_login(login_url)


