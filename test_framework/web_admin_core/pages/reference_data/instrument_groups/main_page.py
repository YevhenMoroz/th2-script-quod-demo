import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.reference_data.instrument_groups.constants import \
    InstrumentGroupsConstants

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class InstrumentGroupsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(InstrumentGroupsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(InstrumentGroupsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(InstrumentGroupsConstants.CLONE_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(InstrumentGroupsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_delete(self, confirmation):
        self.find_by_xpath(InstrumentGroupsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(InstrumentGroupsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(InstrumentGroupsConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_pin_row(self):
        self.find_by_xpath(InstrumentGroupsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(InstrumentGroupsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(InstrumentGroupsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(InstrumentGroupsConstants.LOGOUT_BUTTON_XPATH).click()

    def set_instrument_group(self, value):
        self.set_text_by_xpath(InstrumentGroupsConstants.MAIN_PAGE_INSTRUMENT_GROUP_FILTER_XPATH, value)

    def set_description(self, value):
        self.set_text_by_xpath(InstrumentGroupsConstants.MAIN_PAGE_DESCRIPTION_FILTER_XPATH, value)

    def get_instrument_group(self):
        return self.find_by_xpath(InstrumentGroupsConstants.MAIN_PAGE_INSTRUMENT_GROUP_XPATH).text

    def get_description(self):
        return self.find_by_xpath(InstrumentGroupsConstants.MAIN_PAGE_DESCRIPTION_XPATH).text
