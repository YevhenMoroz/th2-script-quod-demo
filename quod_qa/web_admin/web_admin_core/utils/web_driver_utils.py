from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def find_by_css_selector(web_driver_wait: WebDriverWait, css_selector: str):
    return find_by(web_driver_wait, By.CSS_SELECTOR, css_selector)


def find_by_xpath(web_driver_wait: WebDriverWait, xpath: str):
    return find_by(web_driver_wait, By.XPATH, xpath)


def find_by(web_driver_wait: WebDriverWait, location_strategy: By, locator: str):
    return web_driver_wait.until(expected_conditions.visibility_of_element_located((location_strategy, locator)))
