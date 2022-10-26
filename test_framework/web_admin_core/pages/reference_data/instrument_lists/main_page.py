import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.reference_data.instrument_lists.constants import \
    InstrumentListsConstants

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class InstrumentListsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(InstrumentListsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(InstrumentListsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(InstrumentListsConstants.CLONE_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(InstrumentListsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_delete(self, confirmation):
        self.find_by_xpath(InstrumentListsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(InstrumentListsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(InstrumentListsConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_pin_row(self):
        self.find_by_xpath(InstrumentListsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(InstrumentListsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(InstrumentListsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(InstrumentListsConstants.LOGOUT_BUTTON_XPATH).click()

    def set_instrument_list(self,value):
        pass

    def get_instrument_list(self):
        pass

    def set_venue_instrument_list_id(self,value):
        pass

    def get_venue_instrument_list_id(self):
        pass
