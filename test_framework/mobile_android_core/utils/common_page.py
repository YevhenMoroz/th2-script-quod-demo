from appium_flutter_finder import FlutterElement, FlutterFinder
from test_framework.mobile_android_core.utils.driver import AppiumDriver
from test_framework.mobile_android_core.utils.decorators.find_element_decorator_mobile import wait_for_element
class CommonPage:
    def __init__(self, driver: AppiumDriver):
        """
        class is used to implement all common actions doing with elements on all pages
        :param appium_driver - used to interract with our elements and do actions
        :param finder - used to find elements by different ways, e.g. by value key set on DEV side
        """
        self.appium_driver = driver
        self.finder = FlutterFinder()

    @wait_for_element
    def enter_data(self, key, data):
        """
        method is used to find element by valueKey = key and input data in it
        """
        element = FlutterElement(self.appium_driver.get_driver(), self.finder.by_value_key(key))
        element.send_keys(data)

    @wait_for_element
    def tap(self, key):
        """
        method is used to find element by valueKey = key and tap on it
        """
        element = FlutterElement(self.appium_driver.get_driver(), self.finder.by_value_key(key))
        element.click()

    @wait_for_element
    def get_text(self, key):
        """
        method is used to get text of element
        """
        element = FlutterElement(self.appium_driver.get_driver(), self.finder.by_value_key(key))
        return element.text

    # OLD APPIUM FRAMEWORK METHODS
    # def get_element_exists_by_xpath(self, xpath):
    #     if self.get_count_of_elements_by_xpath(xpath)==0:
    #         return False
    #     else:
    #         return True
    #
    # def get_count_of_elements_by_xpath(self, xpath):
    #     return len(self.appium_driver.get_driver().find_elements(AppiumBy.XPATH, xpath))
    #
    # def find_all_by_xpath(self, xpath):
    #     return self.appium_driver.get_driver().find_elements(AppiumBy.XPATH, xpath)
    #
    # def find_by_xpath(self, xpath):
    #     return self.appium_driver.get_driver().find_element(AppiumBy.XPATH, xpath)
    #
    # def get_attribute_of_element_by_xpath(self, xpath, value):
    #     return self.find_by_xpath(xpath).get_attribute(str(value))
    #
    # def wait_element_presence(self, xpath):
    #     return self.Waiter.wait_until_presence_by_xpath(xpath)
    #
    # def wait_edit_mode(self, xpath):
    #     return self.Waiter.wait_until_attribute_value_equals_by_xpath(xpath, 'focused', 'true')
    #
    # def tap_by_coordinates(self, x, y, count=1):
    #     # TouchAction(driver=self.appium_driver.get_driver()).tap(None, x, y, count).perform()
    #     actions = ActionChains(self.appium_driver.get_driver())
    #     actions.w3c_actions.pointer_action.move_to_location(x, y)
    #     for x in range(count):
    #         actions.w3c_actions.pointer_action.click()
    #     actions.w3c_actions.perform()
    #
    # def swipe_by_coordinates(self, start_x, start_y, end_x, end_y):
    #     # TouchAction(self.appium_driver.get_driver()).long_press(None, start_x, start_y).move_to(None, end_x, end_y).release().perform()
    #     actions = ActionChains(self.appium_driver.get_driver())
    #     actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
    #     actions.w3c_actions.pointer_action.pointer_down()
    #     actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
    #     actions.w3c_actions.pointer_action.pointer_up()
    #     actions.w3c_actions.perform()
    #
    # def go_back(self):
    #     self.appium_driver.get_driver().back()
    #
    # def click_keyboard(self, key):
    #     self.appium_driver.get_driver().press_keycode(self.get_keycode(key))
    #
    # def get_keycode(self, key):
    #     switcher ={
    #         "Back":4,
    #         "Backspace":67,
    #         "Enter":66,
    #         "Space":62
    #     }
    #     return switcher.get(key, "Invalid key constant field")
