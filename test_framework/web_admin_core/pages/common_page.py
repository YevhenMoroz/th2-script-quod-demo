import os
import time
import pyautogui

import pyperclip
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from test_framework.web_admin_core.utils.common_constants import CommonConstants
from test_framework.web_admin_core.utils.csv_utils.csv_reader import CsvReader
from test_framework.web_admin_core.utils.pdf_utils.pdf_reader import PdfReader
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_admin_core.utils.web_driver_utils import delete_all_files_with_extension, \
    find_files_by_extension
from selenium.common.exceptions import NoSuchElementException


def waiting_until_page_requests_to_be_load(function):
    """
    The method will check if all requests for the page have loaded within 1 minute, otherwise we get an exception
    """
    def wrapper(*args):
        self = args[0]
        if self.is_element_present(CommonConstants.USER_ICON) or self.is_element_present(CommonConstants.HELP_ICON):
            a = 0
            while True:
                if "done" not in self.web_driver.find_element(By.XPATH, CommonConstants.PAGE_BODY).get_attribute(
                                    'class'):
                    a += 1
                    time.sleep(0.25)
                elif a == 240: self.web_driver_container.stop_driver()
                else: return function(*args)
        elif not self.is_element_present(CommonConstants.NGX_APP_LOADED):
            a = 0
            while True:
                if not self.is_element_present(CommonConstants.NGX_APP_LOADED):
                    a += 1
                    time.sleep(0.25)
                elif a == 240: self.web_driver_container.stop_driver()
                else: return function(*args)
        else: return function(*args)
    return wrapper


class CommonPage:
    def __init__(self, web_driver_container: WebDriverContainer):
        self.web_driver_container = web_driver_container
        self.web_driver_wait = web_driver_container.get_wait_driver()
        self.web_driver = web_driver_container.get_driver()

    def find_by_css_selector(self, css_selector: str):
        return self.find_by(By.CSS_SELECTOR, css_selector)

    def find_by_xpath(self, xpath: str):
        return self.find_by(By.XPATH, xpath)

    @waiting_until_page_requests_to_be_load
    def find_by(self, location_strategy: By, locator: str):
        element = None
        try:
            element = self.web_driver_wait.until(
                expected_conditions.visibility_of_element_located((location_strategy, locator)))
        except Exception:
            pass
        if element is None:
            raise NoSuchElementException(f"Element by given path {locator} not found")
        else:
            return element

    def find_elements_by_xpath(self, xpath: str):
        return self.find_elements_by(By.XPATH, xpath)

    @waiting_until_page_requests_to_be_load
    def find_elements_by(self, location_strategy: By, locator: str):
        elements = None
        try:
            elements = self.web_driver_wait.until(
                expected_conditions.visibility_of_any_elements_located((location_strategy, locator)))
        except Exception:
            pass
        if elements is None:
            raise NoSuchElementException(f"Elements by given path {locator} not found")
        else:
            return elements

    def get_text_by_xpath(self, xpath: str):
        if "button" in xpath:
            return self.find_by_xpath(xpath).text
        elif self.find_by_xpath(xpath).get_attribute("disabled"):
            element = self.find_by_xpath(xpath)
            action = ActionChains(self.web_driver_container.get_driver())
            action.double_click(element)
            action.click()
            action.key_down(Keys.CONTROL)
            action.send_keys("C")
            action.key_up(Keys.CONTROL)
            action.perform()
            value_from_element = pyperclip.paste()
            return value_from_element
        elif "multiselect" in self.find_by_xpath(xpath).get_attribute("class"):
            return self.find_by_xpath(xpath + CommonConstants.MULTISELECT_ENTITIES).text
        elif "appearance-outline" in self.find_by_xpath(xpath).get_attribute("class"):
            return self.find_by_xpath(xpath + CommonConstants.ENUM_DROP_DOWN).text
        else:
            element = self.find_by_xpath(xpath)
            value_from_clipboard = pyperclip.paste()
            #element.click()
            element.send_keys(Keys.CONTROL, "A")
            element.send_keys(Keys.CONTROL, "C")
            value_from_element = pyperclip.paste()
            pyperclip.copy(value_from_clipboard)
            return value_from_element

    def set_text_by_xpath(self, xpath: str, value: str, is_clear_before: bool = True):
        text_field = self.find_by_xpath(xpath)

        if is_clear_before:
            text_field.send_keys(Keys.CONTROL, "A")
            text_field.send_keys(Keys.DELETE)

        text_field.send_keys(value)

    def set_checkbox_list(self, xpath: str, values: str or list or int):
        """
        Method was created for setting checkbox list,
        concatenates the xpath to the checkbox through its values
        """
        if not self.is_element_present(CommonConstants.COMBOBOX_DROP_DOWN_XPATH):
            self.find_by_xpath(xpath).click()
        time.sleep(1)
        if type(values) != list:
            values = values.split(",")
        [self.find_by_xpath(CommonConstants.COMBOBOX_OPTION_PATTERN_XPATH.format(i)).click() for i in values]
        self.find_by_xpath(xpath).click()

    def set_combobox_value(self, combobox_xpath: str, value: str):
        """
        Method was created for setting value from drop down list
        in active input field.
        """
        self.set_text_by_xpath(combobox_xpath, value)
        time.sleep(1)
        self.find_by_xpath(CommonConstants.COMBOBOX_OPTION_PATTERN_XPATH.format(value)).click()

    def set_multiselect_field_value(self, field_xpath: str, values: str or list or int):
        """
        Method was created for setting checkbox list inside field type of multiselect,
        concatenates the xpath to the checkbox through its values
        """
        self.find_by_xpath(field_xpath).click()
        time.sleep(0.5)
        if not self.is_element_present(CommonConstants.MULTISELECT_FORM_LOOK_UP):
            self.find_by_xpath(field_xpath).click()
        time.sleep(1)
        if type(values) != list:
            values = values.split(",")
        for i in values:
            self.set_text_by_xpath(CommonConstants.MULTISELECT_FORM_LOOK_UP, i)
            time.sleep(0.2)
            self.find_by_xpath(CommonConstants.MULTISELECT_ITEM_XPATH.format(i)).click()
            time.sleep(1)
        self.find_by_xpath(CommonConstants.MULTISELECT_DROP_DOWN_CLOSE_BUTTON).click()
        time.sleep(1)

    def select_value_from_dropdown_list(self, xpath: str, value: str):
        """
        Method was created for select value from dropdown list
        if if there is no input field
        """
        if not self.is_element_present(CommonConstants.GENERAL_DROP_DOWN):
            self.find_by_xpath(xpath).click()
        time.sleep(1)
        self.find_by_xpath(xpath + CommonConstants.DROP_MENU_OPTION_PATTERN_XPATH.format(value, value)).click()

    def is_checkbox_selected(self, checkbox_xpath: str):
        if "custom-checkbox" not in self.find_by_xpath(checkbox_xpath).get_attribute("class"):
            return True if "checked" in self.find_by_xpath(checkbox_xpath+'//span[contains(@class, "custom-checkbox")]')\
                .get_attribute("class") else False
        return True if "checked" in self.find_by_xpath(checkbox_xpath).get_attribute("class") else False

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
        delete_all_files_with_extension(download_directory, ".txt")

    def get_txt_context(self):
        path_to_txt = self.__get_downloaded_file(".txt")

        with open(path_to_txt, "r") as file:
            file_context = file.readlines()
            return file_context

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

    def is_field_enabled(self, xpath):
        return self.find_by_xpath(xpath).is_enabled()

    def is_checkbox_enabled(self, checkbox_xpath):
        return self.find_by_xpath(checkbox_xpath+'//ancestor::nb-checkbox//input').is_enabled()

    def find_element_in_shadow_root(self, css_path):
        '''
        Method was created for searching elements in DOM for #shadow-root tags
        '''
        search_button = self.web_driver.execute_script(css_path)
        return search_button

    def is_element_present(self, xpath):
        try:
            self.web_driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    def use_keyboard_esc_button(self):
        self.find_by_xpath("//body").send_keys(Keys.ESCAPE)

    def use_backspace_button_to_element(self):
        action = ActionChains(self.web_driver)
        action.key_down(Keys.BACK_SPACE)
        action.key_up(Keys.BACK_SPACE)
        action.perform()


    def horizontal_scroll(self, search_element):
        '''
        Method was created for scroll
        '''
        scr_elem = self.find_by_xpath(CommonConstants.HORIZONTAL_SCROLL_ELEMENT_XPATH)
        elem_size = int(scr_elem.size['width'])
        e = self.web_driver.find_element(By.XPATH, CommonConstants.HORIZONTAL_SCROLL_WHEEL).get_attribute('style')
        scr_elem_full_size = int(e.split()[1].replace('px;', ''))
        wheel_position = 0
        if 'transform' in e:
            wheel_position = abs(int(e.split()[-1].replace('translateX(', '').replace('px);', '')))

        action = ActionChains(self.web_driver)
        action.move_to_element_with_offset(scr_elem, 5, 5).perform()
        action.double_click()
        action.double_click()
        time.sleep(0.5)
        c = 0
        if wheel_position != 0:
            c = scr_elem_full_size - elem_size - wheel_position
            d = wheel_position
            while True:
                if d <= wheel_position and c <= elem_size:
                    e = self.web_driver.find_element(By.XPATH, CommonConstants.HORIZONTAL_SCROLL_WHEEL).get_attribute(
                        'style')
                    d = abs(int(e.split()[-1].replace('translateX(', '').replace('px);', '')))
                    c += 100
                    action.move_to_element_with_offset(scr_elem, c, 5).click().perform()
                else:
                    break
        else:
            while elem_size > c:
                action = ActionChains(self.web_driver)
                action.move_to_element_with_offset(scr_elem, c, 5).click().perform()
                c += 100
                e = self.web_driver.find_element(By.XPATH, CommonConstants.HORIZONTAL_SCROLL_WHEEL).get_attribute(
                    'style')
                if self.is_element_present(search_element) and 'transform' in e and '(0px)' not in e:
                    break

    def write_to_file(self, path_to_file, value):
        try:
            with open(path_to_file, "w") as file:
                file.write(value)
        except FileNotFoundError as e:
            print("File with password not found", e.__class__.__name__)
        finally:
            file.close()

    def parse_from_file(self, path_to_file):
        try:
            with open(path_to_file, "r") as file:
                search_value = file.readline()
                return search_value
        except Exception as e:
            print("File with password not found", e.__class__.__name__)
        finally:
            file.close()

    def is_field_required(self, field_xpath):
        '''
        return true if field is required or false if not
        '''
        return self.find_by_xpath(field_xpath).get_attribute("required") == "true"

    def get_all_items_from_drop_down(self, xpath) -> list:
        items = self.find_elements_by_xpath(xpath)
        items_list = [_.text.strip() for _ in items]
        return items_list

    def get_all_items_from_table_column(self, xpath) -> list:
        items = self.find_elements_by_xpath(xpath)
        items_list = [_.text.strip() for _ in items]
        return items_list

    def get_all_checkboxes_statuses_from_table_column(self, xpath) -> list:
        checkboxes = self.find_elements_by_xpath(xpath)
        statuses = [_.is_selected() for _ in checkboxes]
        return statuses

    def set_upload_file_path_and_confirm(self, path_to_file):
        """
        The method is implemented to add the file to the context window that appears,
        which expects the user to path to the file and press the "Enter" button to confirm sending
        """
        pyautogui.write(path_to_file)
        pyautogui.press('enter')
