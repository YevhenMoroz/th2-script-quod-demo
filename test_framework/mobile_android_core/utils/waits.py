from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Waits:

    def __init__(self, driver, time=5):
        self.appium_driver = driver
        self.wait = WebDriverWait(self.appium_driver, time)

    def wait_until_clickable_by_xpath(self, xpath):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

    def wait_until_presence_by_xpath(self, xpath):
        self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    def wait_until_text_is_presented_by_xpath(self, xpath, text):
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath), text))

    def wait_until_attribute_value_equals_by_xpath(self, xpath, attribute, text):
        self.wait.until(EC.text_to_be_present_in_element_attribute((By.XPATH, xpath), attribute, text))

    def wait_until_staleness_by_xpath(self, xpath):
        self.wait.until(EC.staleness_of((By.XPATH, xpath)))
