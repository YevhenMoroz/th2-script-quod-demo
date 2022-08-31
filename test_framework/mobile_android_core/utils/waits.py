from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Waits:

    def __init__(self, driver, time=5):
        self.appium_driver = driver
        self.wait = WebDriverWait(self.appium_driver, time)

    def WaitUntilClickableByXPath(self, xpath):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

    def WaitUntilVisibleByXPath(self, element):
        self.wait.until(EC.visibility_of(element))

