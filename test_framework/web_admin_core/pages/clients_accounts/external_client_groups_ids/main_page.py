import time

from test_framework.web_admin_core.pages.clients_accounts.external_client_groups_ids.constants import \
    ExternalClientGroupIDsConstants
from test_framework.web_admin_core.pages.common_page import CommonPage

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ExternalClientGroupIDsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(ExternalClientGroupIDsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ExternalClientGroupIDsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(ExternalClientGroupIDsConstants.CLONE_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(ExternalClientGroupIDsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_delete(self, confirmation):
        self.find_by_xpath(ExternalClientGroupIDsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(ExternalClientGroupIDsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(ExternalClientGroupIDsConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_pin_row(self):
        self.find_by_xpath(ExternalClientGroupIDsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(ExternalClientGroupIDsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(ExternalClientGroupIDsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(ExternalClientGroupIDsConstants.LOGOUT_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(ExternalClientGroupIDsConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def get_name(self):
        return self.find_by_xpath(ExternalClientGroupIDsConstants.MAIN_PAGE_NAME_XPATH).text

    def set_client_group(self, value):
        self.set_text_by_xpath(ExternalClientGroupIDsConstants.MAIN_PAGE_CLIENT_GROUP_FILTER_XPATH, value)

    def get_client_group(self):
        return self.find_by_xpath(ExternalClientGroupIDsConstants.MAIN_PAGE_CLIENT_GROUP_XPATH).text
