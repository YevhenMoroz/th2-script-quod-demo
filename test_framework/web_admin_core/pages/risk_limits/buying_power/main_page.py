import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.risk_limits.buying_power.constants import Constants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class MainPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(Constants.MainPage.MORE_ACTIONS_BUTTON).click()

    def click_on_edit(self):
        self.find_by_xpath(Constants.MainPage.EDIT_BUTTON).click()

    def click_on_clone(self):
        self.find_by_xpath(Constants.MainPage.CLONE_BUTTON).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(Constants.MainPage.DELETE_BUTTON).click()
        if confirmation:
            self.find_by_xpath(Constants.MainPage.OK_BUTTON).click()
        else:
            self.find_by_xpath(Constants.MainPage.CANCEL_BUTTON).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(Constants.MainPage.DOWNLOAD_PDF_BUTTON).click()
        time.sleep(1)
        return self.is_pdf_contains_value(value)

    def click_download_csv_entity_button_and_check_csv(self):
        self.clear_download_directory()
        self.find_by_xpath(Constants.MainPage.DOWNLOAD_CSV_BUTTON).click()
        time.sleep(1)
        return self.get_csv_context()

    def click_on_pin_row(self):
        self.find_by_xpath(Constants.MainPage.PIN_BUTTON).click()

    def click_on_new_button(self):
        self.find_by_xpath(Constants.MainPage.NEW_BUTTON).click()

    def set_name_filter(self, value):
        self.set_text_by_xpath(Constants.MainPage.NAME_FILTER, value)

    def set_description_filter(self, value):
        self.set_text_by_xpath(Constants.MainPage.DESCRIPTION_FILTER, value)

    def is_searched_entity_found_by_name(self, name):
        return self.is_element_present(Constants.MainPage.SEARCHED_ENTITY.format(name))

    def is_entity_pinned(self, name):
        return self.is_element_present(Constants.MainPage.PINNED_ENTITY.format(name))
