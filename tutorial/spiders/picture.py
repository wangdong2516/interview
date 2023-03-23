import time

import httpx
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium import webdriver


class PictureSpider(scrapy.Spider):
    name = 'picture'
    allowed_domains = ['pic.netbian.com']
    start_urls = ['http://pic.netbian.com/']

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

    def parse(self, response, *args, **kwargs):
        image_urls = response.xpath('//img[contains(@src, "uploads")]/@src').extract()
        domain = 'http://pic.netbian.com'
        for image_url in image_urls:
            url = f'{domain}{image_url}'
            httpx_response = httpx.get(url)
            image_bytes = httpx_response.content
            file_name = image_url.split('/')[-1]
            try:
                with open(f'{str(self.settings["VERIFY_IMAGE_BIG_DIR"])}/{file_name}', 'wb') as f:
                    f.write(image_bytes)
            except Exception as e:
                print(e)

        # 提取下一页链接
        next_page = response.xpath('//a[contains(text(), "下")]/@href').extract()
        for next_ in next_page:
            if next_.startswith('/'):

                next_page_url = f'{domain}{next_}'
                yield SeleniumRequest(url=next_page_url, callback=self.parse)
