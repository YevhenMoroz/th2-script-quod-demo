import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.general.system_components.constants import Constants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class MainPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_full_screen_button(self):
        self.find_by_xpath(Constants.MainPage.FULL_SCREEN_BUTTON).click()

    def click_on_refresh_page_button(self):
        self.find_by_xpath(Constants.MainPage.REFRESH_BUTTON).click()

    def click_on_more_actions(self):
        self.find_by_xpath(Constants.MainPage.MORE_ACTIONS_BUTTON).click()

    def click_on_edit(self):
        self.find_by_xpath(Constants.MainPage.EDIT_BUTTON).click()

    def click_on_pin_row(self):
        self.find_by_xpath(Constants.MainPage.PIN_BUTTON).click()

    def set_instance_id(self, value):
        self.set_text_by_xpath(Constants.MainPage.INSTANCE_ID_FILTER, value)

    def set_short_name(self, value):
        self.set_text_by_xpath(Constants.MainPage.SHORT_NAME_FILTER, value)

    def set_long_name(self, value):
        self.set_text_by_xpath(Constants.MainPage.LONG_NAME_FILTER, value)

    def set_version(self, value):
        self.set_text_by_xpath(Constants.MainPage.VERSION_FILTER, value)

    def set_active(self, value):
        self.set_text_by_xpath(Constants.MainPage.ACTIVE_FILTER, value)

    def is_searched_entity_found_by_name(self, name):
        return self.is_element_present(Constants.MainPage.SEARCHED_ENTITY.format(name))

    def is_entity_pinned(self, name):
        return self.is_element_present(Constants.MainPage.PINNED_ENTITY.format(name))

    def is_active_status_displayed(self):
        return self.is_element_present(Constants.MainPage.ACTIVE_STATUS_ICON)

    def is_site_header_displayed(self):
        return self.is_element_present(Constants.MainPage.SITE_HEADER)

    def is_new_button_displayed(self):
        return self.is_element_present(Constants.MainPage.NEW_BUTTON)

    def is_clone_button_displayed(self):
        return self.is_element_present(Constants.MainPage.CLONE_BUTTON)

    def is_delete_button_displayed(self):
        return self.is_element_present(Constants.MainPage.DELETE_BUTTON)

    def is_download_pdf_button_displayed(self):
        return self.is_element_present(Constants.MainPage.DOWNLOAD_PDF_BUTTON)

    def click_on_download_csv_button_and_get_content(self):
        self.clear_download_directory()
        self.find_by_xpath(Constants.MainPage.DOWNLOAD_CSV_BUTTON).click()
        time.sleep(1)
        return self.get_csv_context()
