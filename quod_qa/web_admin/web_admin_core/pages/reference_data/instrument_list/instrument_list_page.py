import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.instrument_list.instrument_list_constants import \
    InstrumentListConstants

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class InstrumentListPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(InstrumentListConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(InstrumentListConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(InstrumentListConstants.CLONE_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(InstrumentListConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_delete(self, confirmation):
        self.find_by_xpath(InstrumentListConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(InstrumentListConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(InstrumentListConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_pin_row(self):
        self.find_by_xpath(InstrumentListConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(InstrumentListConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(InstrumentListConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(InstrumentListConstants.LOGOUT_BUTTON_XPATH).click()

    def set_instrument_list(self,value):
        pass

    def get_instrument_list(self):
        pass

    def set_venue_instrument_list_id(self,value):
        pass

    def get_venue_instrument_list_id(self):
        pass
