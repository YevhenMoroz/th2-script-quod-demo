from appium import webdriver
from appium.webdriver.appium_service import AppiumService


class AppiumDriver:


    def __init__(self):
        self.appium_driver =None

    def start_appium_service(self):
        global appium_service
        appium_service = AppiumService()
        appium_service.start()
        desired_cap = {}
        desired_cap['platformName'] = 'Android'
        desired_cap['deviceName'] = 'Android'
        desired_cap['appPackage'] = 'com.quod.trading.uat_alrajhitadawul'
        desired_cap['appActivity'] = 'com.quod.moorgate.moorgatemobile.MainActivity'
        self.appium_driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_cap)
        self.appium_driver.implicitly_wait(5)

    def stop_appium_service(self):
        self.appium_driver.quit()
        appium_service.stop()

    def get_driver(self):
        return self.appium_driver

