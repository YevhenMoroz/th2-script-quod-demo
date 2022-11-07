import time

from test_framework.web_admin_core.pages.clients_accounts.client_lists.constants import ClientListsConstants
from test_framework.web_admin_core.pages.common_page import CommonPage

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientListsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(ClientListsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ClientListsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(ClientListsConstants.CLONE_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(ClientListsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_delete(self, confirmation):
        self.find_by_xpath(ClientListsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(ClientListsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(ClientListsConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_pin_row(self):
        self.find_by_xpath(ClientListsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(ClientListsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(ClientListsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(ClientListsConstants.LOGOUT_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(ClientListsConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def get_name(self):
        return self.find_by_xpath(ClientListsConstants.MAIN_PAGE_NAME_XPATH).text

    def set_description(self, value):
        self.set_text_by_xpath(ClientListsConstants.MAIN_PAGE_DESCRIPTION_FILTER_XPATH, value)

    def get_description(self):
        return self.find_by_xpath(ClientListsConstants.MAIN_PAGE_DESCRIPTION_XPATH).text

    def is_client_list_found(self, value):
        return self.is_element_present(ClientListsConstants.DISPLAYED_CLIENT_LIST_XPATH.format(value))
