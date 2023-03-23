import time

import scrapy
from scrapy import Request
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class MedrioSpider(scrapy.Spider):
    name = 'medrio'
    # allowed_domains = []
    start_urls = ['https://identity.medrio.com/identity/login?signin=2c3524f98360476749b730d711158f49']

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url)

    def parse(self, response, *args, **kwargs):
        browser = self.create_webdriver(self.settings['SELENIUM_DRIVER_EXECUTABLE_PATH'])
        browser.get(url=response.url)
        browser.find_element(by=By.XPATH, value='//input[@name="username_"]').send_keys('gsbtest')
        browser.find_element(by=By.XPATH, value='//input[@name="password"]').send_keys('dip@123456')
        browser.find_element(by=By.XPATH, value='//input[@id="btnLogin"]').click()
        browser.get(url='https://login.medrio.com/Account/Profile?returnURL=https%3a%2f%2fapac01.medrio.com%2fMedrioWeb%2fapp%2fmanage%2fdefault.aspx%3finit%3dtrue')  # noqa:E501
        browser.get(url='https://login.medrio.com/Account/AddPhoneNumber?ReturnUrl=https%3A%2F%2Fapac01.medrio.com%2FMedrioWeb%2Fapp%2Fmanage%2Fdefault.aspx%3Finit%3Dtrue')  # noqa:E501
        # 国家名称
        browser.find_element(by=By.XPATH, value='//div[@class="flag-container"]').click()
        country_names_ele = browser.find_elements(by=By.CLASS_NAME, value='country')
        dial_code_ele = browser.find_elements(by=By.CLASS_NAME, value='dial-code')
        country_code_ele = browser.find_elements(by=By.CLASS_NAME, value='country')
        country_names = []
        dial_codes = []
        country_codes = []
        for country in country_names_ele:
            country_names.append(country.text)
        for dial_code in dial_code_ele:
            dial_codes.append(dial_code.text)
        for countrycode in country_code_ele:
            country_codes.append(countrycode.get_attribute('data-country-code'))
        for country_name, dial_code, country_code in list(zip(country_names, dial_codes, country_codes)):
            with open('./country_dial_code.sql', 'a') as f:
                f.writelines(
                    f"INSERT INTO `country_dial_code` (`country_name`, `dial_code`, `country_code`) VALUE ("
                    f"'{country_name.split('+')[0].strip('RLEPDF')}', {dial_code.strip('+')}, '{country_code}');\n")
        browser.quit()

    @staticmethod
    def create_webdriver(executable_path: str) -> webdriver.Chrome:

        """
        创建浏览器驱动
        Args:
            executable_path: 浏览器驱动的可执行路径

        Returns:

        """
        options = webdriver.ChromeOptions()
        options.add_argument("--proxy-server=http://127.0.0.1:7890")
        driver = webdriver.Chrome(options=options, executable_path=executable_path)
        return driver
