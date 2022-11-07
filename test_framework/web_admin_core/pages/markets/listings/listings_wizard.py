import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.listings.listings_constants import ListingsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingsWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(ListingsConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(ListingsConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def is_save_button_enabled(self):
        return self.find_by_xpath(ListingsConstants.SAVE_CHANGES_BUTTON_XPATH).is_enabled()

    def click_on_revert_changes(self):
        self.find_by_xpath(ListingsConstants.REVERT_CHANGES_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(ListingsConstants.DOWNLOAD_PDF_AT_WIZARD_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_go_back_button(self):
        self.find_by_xpath(ListingsConstants.GO_BACK_BUTTON_XPATH).click()

    def click_on_ok_button(self):
        self.find_by_xpath(ListingsConstants.OK_BUTTON_XPATH).click()

    def get_error_message_inside_listing_wizard(self):
        return self.find_by_xpath(ListingsConstants.ERROR_MESSAGE_WIZARD_XPATH).text

    def is_error_message_displayed(self):
        return self.is_element_present(ListingsConstants.ERROR_MESSAGE_WIZARD_XPATH)

    def is_request_failed_message_displayed(self):
        return self.find_by_xpath(ListingsConstants.REQUEST_FAILED_MESSAGE_XPATH).is_displayed()

