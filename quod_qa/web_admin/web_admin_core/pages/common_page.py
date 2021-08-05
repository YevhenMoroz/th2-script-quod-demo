import os

import pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select

from typing import List

from quod_qa.web_admin.web_admin_core.utils.common_constants import CommonConstants
from quod_qa.web_admin.web_admin_core.utils.csv_utils.csv_reader import CsvReader
from quod_qa.web_admin.web_admin_core.utils.pdf_utils.pdf_reader import PdfReader
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_core.utils.web_driver_utils import delete_all_files_with_extension, \
    find_files_by_extension


class CommonPage:
    def __init__(self, web_driver_container: WebDriverContainer):
        self.web_driver_container = web_driver_container
        self.web_driver_wait = web_driver_container.get_wait_driver()

    def find_by_css_selector(self, css_selector: str):
        return self.find_by(By.CSS_SELECTOR, css_selector)

    def find_by_xpath(self, xpath: str):
        return self.find_by(By.XPATH, xpath)

    def find_by(self, location_strategy: By, locator: str):
        return self.web_driver_wait.until(
            expected_conditions.visibility_of_element_located((location_strategy, locator)))

    # .text does not work
    def get_text_by_xpath(self, xpath: str):
        element = self.find_by_xpath(xpath)

        value_from_clipboard = pyperclip.paste()
        element.click()
        element.send_keys(Keys.CONTROL, "A")
        element.send_keys(Keys.CONTROL, "C")

        value_from_element = pyperclip.paste()

        pyperclip.copy(value_from_clipboard)
        return value_from_element

    def set_text_by_xpath(self, xpath: str, value: str, is_clear_before: bool = True):
        text_field = self.find_by_xpath(xpath)

        # .clear() does not work
        if is_clear_before:
            text_field.send_keys(Keys.CONTROL, "A")
            text_field.send_keys(Keys.DELETE)

        text_field.send_keys(value)

    def set_checkbox_list(self, checkbox_xpath: str, values: tuple):
        """
        Method was created for setting checkbox list,
        concatenates the xpath to the checkbox through its values
        """
        result = list(values)
        result.clear()
        for item in range(len(values)):
            result.append(checkbox_xpath.format(values[item]))
        return result

    def set_combobox_value(self, combobox_xpath: str, value: str):
        self.set_text_by_xpath(combobox_xpath, value)

        option_xpath = CommonConstants.COMBOBOX_OPTION_PATTERN_XPATH.format(value)
        option = self.find_by_xpath(option_xpath)
        option.click()

    def select_value_from_dropdown_list(self, xpath: str, value: str):
        """
        Method was created for select value from dropdown list
        if if there is no input field
        """
        select = Select(self.find_by_xpath(xpath))
        select.select_by_value(value)

    def is_checkbox_selected(self, checkbox_xpath: str):
        checkbox_state_span = self.get_checkbox_state_span(checkbox_xpath)
        checkbox_state_span_attribute = checkbox_state_span.get_attribute("class")

        return CommonConstants.CHECKED_ATTRIBUTE in checkbox_state_span_attribute

    def toggle_checkbox(self, checkbox_xpath: str):
        checkbox_state_span = self.get_checkbox_state_span(checkbox_xpath)
        checkbox_state_span.click()

    def get_checkbox_state_span(self, checkbox_xpath: str):
        checkbox = self.find_by_xpath(checkbox_xpath)
        return checkbox.find_element_by_css_selector(CommonConstants.COMMON_CHECKBOX_STATE_SPAN_CSS_SELECTOR)

    def is_toggle_button_enabled(self, checkbox_xpath: str):
        toggle_button = self.find_by_xpath(checkbox_xpath)
        toggle_button_state_attribute = toggle_button.get_attribute("class")

        return CommonConstants.CHECKED_ATTRIBUTE in toggle_button_state_attribute

    def clear_download_directory(self):
        download_directory = self.web_driver_container.download_dir

        delete_all_files_with_extension(download_directory, ".pdf")
        delete_all_files_with_extension(download_directory, ".csv")

    def get_csv_context(self):
        path_to_csv = self.__get_downloaded_file(".csv")

        csv_reader = CsvReader(path_to_csv)
        return csv_reader.read_csv_content()

    def is_pdf_contains_value(self, value):
        path_to_pdf = self.__get_downloaded_file(".pdf")

        pdf_reader = PdfReader(path_to_pdf)
        return pdf_reader.is_contains(value)

    def __get_downloaded_file(self, extension: str):
        download_directory = self.web_driver_container.download_dir

        files = find_files_by_extension(download_directory, extension)

        if len(files) > 1:
            raise ValueError(f"In the download directory found several {extension} files, but must be only one!")

        return os.path.join(download_directory, files.pop(0))



