import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.risk_limits.external_check.external_check_constants import \
    ExternalCheckConstants

from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ExternalCheckPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(ExternalCheckConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ExternalCheckConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(ExternalCheckConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(ExternalCheckConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(ExternalCheckConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(ExternalCheckConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(ExternalCheckConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row(self):
        self.find_by_xpath(ExternalCheckConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(ExternalCheckConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(ExternalCheckConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(ExternalCheckConstants.LOGOUT_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(ExternalCheckConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def set_client(self, value):
        self.set_text_by_xpath(ExternalCheckConstants.MAIN_PAGE_CLIENT_FILTER_XPATH, value)

    def set_instr_type(self, value):
        self.set_text_by_xpath(ExternalCheckConstants.MAIN_PAGE_INSTR_TYPE_FILTER_XPATH, value)

    def set_venue(self, value):
        self.set_text_by_xpath(ExternalCheckConstants.MAIN_PAGE_VENUE_FILTER_XPATH, value)

    def set_client_group(self, value):
        self.set_text_by_xpath(ExternalCheckConstants.MAIN_PAGE_CLIENT_GROUP_FILTER_XPATH, value)

    def get_name(self):
        return self.find_by_xpath(ExternalCheckConstants.MAIN_PAGE_NAME_XPATH).text

    def get_client(self):
        return self.find_by_xpath(ExternalCheckConstants.MAIN_PAGE_CLIENT_XPATH).text

    def get_instr_type(self):
        return self.find_by_xpath(ExternalCheckConstants.MAIN_PAGE_INSTR_TYPE_XPATH).text

    def get_venue(self):
        return self.find_by_xpath(ExternalCheckConstants.MAIN_PAGE_VENUE_XPATH).text

    def get_client_group(self):
        return self.find_by_xpath(ExternalCheckConstants.MAIN_PAGE_CLIENT_GROUP_XPATH).text
