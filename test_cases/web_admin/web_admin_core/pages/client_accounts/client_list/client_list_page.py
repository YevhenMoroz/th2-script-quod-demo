import time

from test_cases.web_admin.web_admin_core.pages.client_accounts.client_list.client_list_constants import ClientListConstants
from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage

from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientListPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(ClientListConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ClientListConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(ClientListConstants.CLONE_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(ClientListConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_delete(self, confirmation):
        self.find_by_xpath(ClientListConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(ClientListConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(ClientListConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_pin_row(self):
        self.find_by_xpath(ClientListConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(ClientListConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(ClientListConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(ClientListConstants.LOGOUT_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(ClientListConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def get_name(self):
        return self.find_by_xpath(ClientListConstants.MAIN_PAGE_NAME_XPATH).text

    def set_description(self, value):
        self.set_text_by_xpath(ClientListConstants.MAIN_PAGE_DESCRIPTION_FILTER_XPATH, value)

    def get_description(self):
        return self.find_by_xpath(ClientListConstants.MAIN_PAGE_DESCRIPTION_XPATH).text
