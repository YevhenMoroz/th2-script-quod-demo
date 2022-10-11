import json
import time

from stubs import ROOT_DIR
from appium import webdriver
from appium.webdriver.appium_service import AppiumService

class AppiumDriver:


    def __init__(self):
        self.appium_driver = None

    def start_appium_service(self):
        global appium_service
        appium_service = AppiumService()
        appium_service.start()
        # region of starting configured device with configured application
        with open(f'{ROOT_DIR}\\test_framework\\mobile_android_core\\utils\\mobile_configs\\mobile_config_app.json') as json_file:
            app_data = json.load(json_file)
        with open(f'{ROOT_DIR}\\test_framework\\mobile_android_core\\utils\\mobile_configs\\mobile_config_device.json') as json_file:
            device_data = json.load(json_file)
        desired_cap = {**device_data[device_data['currentDevice']], **app_data[app_data['currentApp']]}
        self.appium_driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_cap)
        self.wait_time(5)
        # endregion

    def stop_appium_service(self):
        self.appium_driver.quit()
        appium_service.stop()

    def wait_time(self, time=5):
        self.appium_driver.implicitly_wait(time)

    def get_driver(self):
        return self.appium_driver

