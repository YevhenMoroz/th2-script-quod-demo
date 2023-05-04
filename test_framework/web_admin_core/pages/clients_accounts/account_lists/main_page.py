import time

from test_framework.web_admin_core.pages.clients_accounts.account_lists.constants import Constants
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class MainPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(Constants.MainPage.MORE_ACTIONS_BUTTON).click()

    def click_on_edit(self):
        self.find_by_xpath(Constants.MainPage.EDIT_BUTTON).click()

    def click_on_clone(self):
        self.find_by_xpath(Constants.MainPage.CLONE_BUTTON).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(Constants.MainPage.DOWNLOAD_PDF_BUTTON).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_delete(self, confirmation):
        self.find_by_xpath(Constants.MainPage.DELETE_BUTTON).click()
        if confirmation:
            self.find_by_xpath(Constants.MainPage.OK_BUTTON).click()
        else:
            self.find_by_xpath(Constants.MainPage.CANCEL_BUTTON).click()

    def click_on_pin_row(self):
        self.find_by_xpath(Constants.MainPage.PIN_ROW_BUTTON).click()

    def click_on_new(self):
        self.find_by_xpath(Constants.MainPage.NEW_BUTTON).click()

    def set_name(self, value):
        self.set_text_by_xpath(Constants.MainPage.NAME_FILTER, value)

    def is_account_list_found(self, acc_list_name):
        return self.is_element_present(Constants.MainPage.DISPLAYED_ACCOUNT_LIST.format(acc_list_name))
