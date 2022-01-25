import os
from os import path
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverContainer:
    TIMEOUT_DELAY = 15

    DOWNLOAD_DIRECTORY_NAME = "downloads"

    def __init__(self, url="http://10.0.22.38:3480/quodadmin/saturn/#/auth/login"):
        current_dir = os.getcwd()
        self.download_dir = os.path.join(current_dir, self.DOWNLOAD_DIRECTORY_NAME)

        self.__create_dir_if_not_exist(self.download_dir)

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option('prefs', {'plugins.always_open_pdf_externally': True,
                                                              'download.default_directory': self.download_dir})
        self.initial_url = url
        self.chrome_driver = None
        self.wait_driver = None

    def start_driver(self):
        self.chrome_driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.chrome_options)
        self.wait_driver = WebDriverWait(self.chrome_driver, self.TIMEOUT_DELAY)

        self.chrome_driver.maximize_window()
        self.chrome_driver.get(self.initial_url)

    def get_driver(self):
        return self.chrome_driver

    def get_wait_driver(self):
        return self.wait_driver

    def stop_driver(self):
        self.chrome_driver.close()

    def __create_dir_if_not_exist(self, directory: str):
        if not path.isdir(directory):
            os.mkdir(directory)
