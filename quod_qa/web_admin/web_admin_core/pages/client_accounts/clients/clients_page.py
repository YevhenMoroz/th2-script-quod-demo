import time

from quod_qa.web_admin.web_admin_core.pages.client_accounts.clients.clients_constants import ClientsConstants
from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_enable_disable(self):
        self.find_by_xpath(ClientsConstants.ENABLE_DISABLE_TOGGLE_BUTTON_XPATH).click()

    def click_on_more_actions(self):
        self.find_by_xpath(ClientsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ClientsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(ClientsConstants.CLONE_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(ClientsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row(self):
        self.find_by_xpath(ClientsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(ClientsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(ClientsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(ClientsConstants.LOGOUT_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(ClientsConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def set_description(self, value):
        self.set_text_by_xpath(ClientsConstants.MAIN_PAGE_DESCRIPTION_FILTER_XPATH, value)

    def set_clearing_account_type(self, value):
        self.set_text_by_xpath(ClientsConstants.MAIN_PAGE_CLEARING_ACCOUNT_TYPE_FILTER_XPATH, value)

    def set_booking_ins(self, value):
        self.set_text_by_xpath(ClientsConstants.MAIN_PAGE_BOOKING_INS_FILTER_XPATH, value)

    def set_allocation_preference(self, value):
        self.set_text_by_xpath(ClientsConstants.MAIN_PAGE_ALLOCATION_PREFERENCE_FILTER_XPATH, value)

    def set_disclose_exec(self, value):
        self.set_text_by_xpath(ClientsConstants.MAIN_PAGE_DISCLOSE_EXEC_FILTER_XPATH, value)

    def set_client_group(self, value):
        self.set_text_by_xpath(ClientsConstants.MAIN_PAGE_CLIENT_GROUP_FILTER_XPATH, value)
