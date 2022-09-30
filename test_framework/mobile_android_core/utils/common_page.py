from appium.webdriver.common.mobileby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

from test_framework.mobile_android_core.utils.driver import AppiumDriver
from appium.webdriver.common.touch_action import TouchAction
from test_framework.mobile_android_core.utils.waits import Waits

class CommonPage:
    def __init__(self, driver: AppiumDriver):
        self.appium_driver = driver
        self.Waiter = Waits(self.appium_driver.appium_driver, 10)

    def get_element_exists_by_xpath(self, xpath):
        if self.get_count_of_elements_by_xpath(xpath)==0:
            return False
        else:
            return True

    def get_count_of_elements_by_xpath(self, xpath):
        return len(self.appium_driver.get_driver().find_elements(AppiumBy.XPATH, xpath))

    def find_all_by_xpath(self, xpath):
        return self.appium_driver.get_driver().find_elements(AppiumBy.XPATH, xpath)

    def find_by_xpath(self, xpath):
        return self.appium_driver.get_driver().find_element(AppiumBy.XPATH, xpath)

    def find_by_class(self, class_name):
        return self.appium_driver.get_driver().find_element(AppiumBy.CLASS_NAME, class_name)

    def find_by_accessibility_id(self, id):
        return self.appium_driver.get_driver().find_element(AppiumBy.ACCESSIBILITY_ID, id)

    def find_by_link_text(self, text):
        return self.appium_driver.get_driver().find_element(AppiumBy.LINK_TEXT)

    def get_attribute_of_element_by_xpath(self, xpath, value):
        return self.find_by_xpath(xpath).get_attribute(str(value))

    def wait_element_presence(self, xpath):
        return self.Waiter.wait_until_presence_by_xpath(xpath)

    def wait_element_is_clickable(self, xpath):
        return self.Waiter.wait_until_clickable_by_xpath(xpath)

    def wait_edit_mode(self, xpath):
        return self.Waiter.wait_until_attribute_value_equals_by_xpath(xpath, 'focused', 'true')

    def tap_by_coordinates(self, x, y, count=1):
        # TouchAction(driver=self.appium_driver.get_driver()).tap(None, x, y, count).perform()
        actions = ActionChains(self.appium_driver.get_driver())
        actions.w3c_actions.pointer_action.move_to_location(x, y)
        for x in range(count):
            actions.w3c_actions.pointer_action.click()
        actions.w3c_actions.perform()

    def swipe_by_coordinates(self, start_x, start_y, end_x, end_y):
        # TouchAction(self.appium_driver.get_driver()).long_press(None, start_x, start_y).move_to(None, end_x, end_y).release().perform()
        actions = ActionChains(self.appium_driver.get_driver())
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
        actions.w3c_actions.pointer_action.pointer_up()
        actions.w3c_actions.perform()

    def reorder_by_coordinates(self, start_x, start_y, end_x, end_y):
        # TouchAction(self.appium_driver.get_driver()).long_press(None, start_x, start_y, 4000).move_to(None, end_x, end_y).release().perform()
        actions = ActionChains(self.appium_driver.get_driver())
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(2)
        actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
        actions.w3c_actions.pointer_action.pointer_up()
        actions.w3c_actions.perform()

    def swipe_right_to_left(self):
        device_size = self.appium_driver.get_driver().get_window_size()
        screen_width = device_size['width']
        screen_height = device_size['height']
        start_x = screen_width - 2
        end_x = screen_width / 9
        start_y = screen_height / 2
        end_y = screen_height / 2
        # actions = TouchAction(self.appium_driver.get_driver())
        # actions.long_press(None, start_x, start_y).move_to(None, end_x, end_y).release().perform()
        actions = ActionChains(self.appium_driver.get_driver())
        # actions.w3c_actions = ActionBuilder(self.appium_driver.get_driver(),
        #                                     mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
        actions.w3c_actions.pointer_action.pointer_up()
        actions.w3c_actions.perform()

    def swipe_left_to_right(self):
        device_size = self.appium_driver.get_driver().get_window_size()
        screen_width = device_size['width']
        screen_height = device_size['height']
        start_x = 2
        end_x = screen_width * 8 / 9
        start_y = screen_height / 2
        end_y = screen_height / 2
        # actions = TouchAction(self.appium_driver.get_driver())
        # actions.long_press(None, start_x, start_y).move_to(None, end_x, end_y).release().perform()
        actions = ActionChains(self.appium_driver.get_driver())
        # actions.w3c_actions = ActionBuilder(self.appium_driver.get_driver(),
        #                                     mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
        actions.w3c_actions.pointer_action.pointer_up()
        actions.w3c_actions.perform()

    def go_back(self):
        self.appium_driver.get_driver().back()

    def click_keyboard(self, key):
        self.appium_driver.get_driver().press_keycode(self.get_keycode(key))

    def get_keycode(self, key):
        switcher ={
            "Back":4,
            "Backspace":67,
            "Enter":66,
            "Space":62
        }
        return switcher.get(key, "Invalid key constant field")
