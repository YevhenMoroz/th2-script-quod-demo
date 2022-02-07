import os
from os import path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import xml.etree.ElementTree as ET


class WebDriverContainer:
    TIMEOUT_DELAY = 15

    DOWNLOAD_DIRECTORY_NAME = "downloads"
    CONFIG_FILE_PATH = "..\\test_framework\web_trading\web_trading_core\pages\config.xml"

    def __init__(self, browser, url):
        current_dir = os.getcwd()
        self.download_dir = os.path.join(current_dir, self.DOWNLOAD_DIRECTORY_NAME)

        self.__create_dir_if_not_exist(self.download_dir)
        self.initial_url = url
        self.web_driver = None
        self.wait_driver = None
        self.browser = browser

    def parse_data_from_config_file(self, value):

        tree = ET.parse(open(self.CONFIG_FILE_PATH))
        root = tree.getroot()

        result_tag = root.find(value)
        return str(result_tag.text)

    def start_driver(self):
        try:
            if self.browser == 'Chrome':
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_experimental_option('prefs', {'plugins.always_open_pdf_externally': True,
                                                                 'download.default_directory': self.download_dir})
                self.web_driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
                self.wait_driver = WebDriverWait(self.web_driver, self.TIMEOUT_DELAY)
                self.web_driver.maximize_window()
                site_url = self.parse_data_from_config_file(self.initial_url)
                self.web_driver.get(site_url)

            elif self.browser == 'Firefox':

                options_firefox = webdriver.FirefoxOptions()
                options_firefox.set_preference('browser.download.dir', self.download_dir)
                self.web_driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),
                                                    options=options_firefox,service_log_path=os.devnull)
                self.wait_driver = WebDriverWait(self.web_driver, self.TIMEOUT_DELAY)
                self.web_driver.maximize_window()
                site_url = self.parse_data_from_config_file(self.initial_url)
                self.web_driver.get(site_url)
        except Exception as e:
            print("Web Browser NOT found!\n" + e.__class__.__name__)

    def get_driver(self):
        return self.web_driver

    def get_wait_driver(self):
        return self.wait_driver

    def stop_driver(self):
        self.web_driver.close()

    def __create_dir_if_not_exist(self, directory: str):
        if not path.isdir(directory):
            os.mkdir(directory)
