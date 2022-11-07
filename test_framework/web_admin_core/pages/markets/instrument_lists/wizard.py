import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.instrument_lists.constants import \
    InstrumentListsConstants

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class InstrumentListsWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(InstrumentListsConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(InstrumentListsConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(InstrumentListsConstants.REVERT_CHANGES_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(InstrumentListsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_go_back_button(self):
        self.find_by_xpath(InstrumentListsConstants.GO_BACK_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(InstrumentListsConstants.WIZARD_NAME_XPATH, value)

    def get_name(self):
        self.get_text_by_xpath(InstrumentListsConstants.WIZARD_NAME_XPATH)

    def set_venue_instrument_list_id(self, value):
        self.set_text_by_xpath(InstrumentListsConstants.WIZARD_VENUE_INSTRUMENT_LIST_ID_XPATH, value)

    def get_venue_instrument_list_id(self):
        return self.get_text_by_xpath(InstrumentListsConstants.WIZARD_VENUE_INSTRUMENT_LIST_ID_XPATH)
