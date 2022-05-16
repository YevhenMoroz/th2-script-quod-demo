from appium.webdriver.common.mobileby import AppiumBy
from test_framework.mobile_android_core.utils.driver import AppiumDriver
from appium.webdriver.common.touch_action import TouchAction


class CommonPage:
    def __init__(self, driver: AppiumDriver):
        self.appium_driver = driver

    def find_by_xpath(self, xpath):
        return self.appium_driver.get_driver().find_element_by_xpath(xpath)

    def find_by_class(self, class_name):
        return self.appium_driver.get_driver().find_element(AppiumBy.CLASS_NAME, class_name)

    def find_by_accessibility_id(self, id):
        return self.appium_driver.get_driver().find_element(AppiumBy.ACCESSIBILITY_ID, id)

    def tap_by_coordinates(self, x, y):
        TouchAction(driver=self.appium_driver.get_driver()).tap(x, y).perform()

    def get_attribute_of_element_by_xpath(self, xpath, element):
        return self.find_by_xpath(xpath).get_attribute(str(element))

    #TODO: there must be determined coordinate (x,y)
    def swipe_right_to_left(self):
        device_size = self.appium_driver.get_driver().get_window_size()
        screen_width = device_size['width']
        screen_height = device_size['height']
        start_x = screen_width * 8 / 9
        end_x = screen_width / 9
        start_y = screen_height / 2
        end_y = screen_height / 2
        actions = TouchAction(self.appium_driver.get_driver())
        actions.long_press(None, start_x, start_y).move_to(None, end_x, end_y).release().perform()
