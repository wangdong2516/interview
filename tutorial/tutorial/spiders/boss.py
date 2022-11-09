import time

import scrapy
import re
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.common.by import By
import httpx


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
    def handle_verify_image_ocr(verify_image_src):
        """
            处理图片验证码图片文字识别
        Args:
            verify_image_src: 图片验证码url

        Returns:

        """
        # 下载图片
        response = httpx.get(url=verify_image_src, timeout=5)
        if not response.status_code == 200:
            print('请求失败')
        image_bytes = response.content
        image_suffix = re.sub(r'\?.*', '', verify_image_src.split('.')[-1])
        print(image_suffix)
        image_prefix = re.search(r'=(.*)', verify_image_src).groups()[0] if re.search(r'=(.*)', verify_image_src).groups()[0] else f'unknown{time.ctime()}'
        # 保存图片
        with open(f'./{image_prefix}.{image_suffix}', 'wb') as f:
            f.write(image_bytes)

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
        browser.implicitly_wait(10)

        # 验证图片的地址
        verify_image_src = ''
        try:
            slipper_background_image = browser.find_element(by=By.XPATH, value='//img[@class="yidun_bg-img"]')
            verify_image_src = slipper_background_image.get_attribute('src')
        except Exception as e:
            print('不是滑块验证方式')
        try:
            background_image = browser.find_element(by=By.XPATH, value='//div[@class="geetest_item_wrap"]')
            content = background_image.get_attribute('style')
            verify_image_src = self.extract_verify_image_src(content)
            self.handle_verify_image_ocr(verify_image_src)
        except Exception as e:
            print('不是图形验证码验证方式')

        # browser.find_element(by=By.XPATH, value='//button[@class="btn btn-sms"]').click()

    def parse(self, response, **kwargs):
        """
            在生成response请求之后处理(调用)
        """
        # 提取boss页面的登录链接
        login_url = response.xpath('//a[@ka="header-login"]/@href').extract()[0]
        # 使用验证码方式登录boss
        self.verify_code_login(login_url)


