import time

from test_framework.web_admin_core.pages.clients_accounts.account_lists.constants import Constants
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class Wizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close_wizard(self):
        self.find_by_xpath(Constants.Wizard.CLOSE_WIZARD_BUTTON).click()

    def click_on_save_changes(self):
        self.find_by_xpath(Constants.Wizard.SAVE_CHANGES_BUTTON).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(Constants.Wizard.REVERT_CHANGES).click()

    def click_on_clear_changes(self):
        self.find_by_xpath(Constants.Wizard.CLEAR_CHANGES_BUTTON).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(Constants.Wizard.DOWNLOAD_PDF_BUTTON).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def set_account_list_name(self, value):
        self.set_text_by_xpath(Constants.Wizard.ACCOUNT_LIST_NAME, value)

    def get_account_list_name(self):
        return self.get_text_by_xpath(Constants.Wizard.ACCOUNT_LIST_NAME)

    def click_on_plus(self):
        self.find_by_xpath(Constants.Wizard.PLUS_BUTTON).click()

    def click_on_checkmark(self):
        self.find_by_xpath(Constants.Wizard.CHECKMARK_BUTTON).click()

    def click_on_close(self):
        self.find_by_xpath(Constants.Wizard.CLOSE_WIZARD_BUTTON).click()

    def click_on_edit(self):
        self.find_by_xpath(Constants.Wizard.EDIT_BUTTON).click()

    def click_on_delete(self):
        self.find_by_xpath(Constants.Wizard.DELETE_BUTTON).click()

    def set_account(self, value):
        self.set_combobox_value(Constants.Wizard.ACCOUNT, value)

    def get_account(self):
        return self.get_text_by_xpath(Constants.Wizard.ACCOUNT)

    def get_all_accounts_from_table(self):
        return self.get_all_items_from_table_column(Constants.Wizard.DISPLAYED_ACCOUNTS_IN_TABLE)

    def set_account_filter(self, value):
        self.set_text_by_xpath(Constants.Wizard.ACCOUNT_FILTER, value)

    def click_at_account_link(self):
        self.find_by_xpath(Constants.Wizard.ACCOUNT_LINK_NAME).click()

    def click_on_no_button(self):
        self.find_by_xpath(Constants.Wizard.NO_BUTTON).click()

    def click_on_ok_button(self):
        self.find_by_xpath(Constants.Wizard.OK_BUTTON).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(Constants.Wizard.CANCEL_BUTTON).click()
