import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.reference_data.instrument_group.instrument_group_constants import \
    InstrumentGroupConstants

from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class InstrumentGroupPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(InstrumentGroupConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(InstrumentGroupConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(InstrumentGroupConstants.CLONE_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(InstrumentGroupConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_delete(self, confirmation):
        self.find_by_xpath(InstrumentGroupConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(InstrumentGroupConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(InstrumentGroupConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_pin_row(self):
        self.find_by_xpath(InstrumentGroupConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(InstrumentGroupConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(InstrumentGroupConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(InstrumentGroupConstants.LOGOUT_BUTTON_XPATH).click()

    def set_instrument_group(self, value):
        self.set_text_by_xpath(InstrumentGroupConstants.MAIN_PAGE_INSTRUMENT_GROUP_FILTER_XPATH, value)

    def set_description(self, value):
        self.set_text_by_xpath(InstrumentGroupConstants.MAIN_PAGE_DESCRIPTION_FILTER_XPATH, value)

    def get_instrument_group(self):
        return self.find_by_xpath(InstrumentGroupConstants.MAIN_PAGE_INSTRUMENT_GROUP_XPATH).text

    def get_description(self):
        return self.find_by_xpath(InstrumentGroupConstants.MAIN_PAGE_DESCRIPTION_XPATH).text
