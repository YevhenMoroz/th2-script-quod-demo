import json
import time

from stubs import ROOT_DIR
from appium.webdriver.webdriver import WebDriver
from appium import webdriver
from appium.webdriver.appium_service import AppiumService

class AppiumDriver:

    def __init__(self):
        """
        class is used to describe logic of communication between server, device and application
        """
        self.appium_driver = None

    def start_appium_service(self):
        """
        used to filter focused capabilities and then connect to the application via device and server
        """
        global appium_service
        # region of starting configured device with configured application
        with open(f'{ROOT_DIR}\\test_framework\\mobile_android_core\\utils\\mobile_configs\\mobile_config_app.json') as json_file:
            app_data = json.load(json_file)
        with open(f'{ROOT_DIR}\\test_framework\\mobile_android_core\\utils\\mobile_configs\\mobile_config_device.json') as json_file:
            device_data = json.load(json_file)
        desired_cap = {**device_data[device_data['currentDevice']], **app_data[app_data['currentApp']], "automationName": "flutter", "retryBackoffTime": 5000}
        self.appium_driver = webdriver.Remote('http://127.0.0.1:4723', desired_cap)
        time.sleep(20)
        self.wait_time(5)
        # endregion

    def stop_appium_service(self):
        """
        quit application and server communication method
        """
        self.appium_driver.quit()
        appium_service.stop()

    def wait_time(self, time=5):
        """
        custom method is used to wait action to be able done before raising exception
        """
        self.appium_driver.implicitly_wait(time)

    def get_driver(self):
        """
        used to link the driver for different methods described on another files in repository
        """
        return self.appium_driver

