import scrapy


class ToutiaoSpider(scrapy.Spider):
    """
        今日头条新闻网站的爬虫
    """
    name = "toutiao"
    allowed_domains = ["www.toutiao.com"]
    start_urls = ["http://www.toutiao.com/"]

    def parse(self, response):
        print(response.text)
