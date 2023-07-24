import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.users.user_lists.constants import Constants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class Wizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_header_link(self):
        self.find_by_xpath(Constants.Wizard.HEADER_LINK).click()

    def click_on_help_icon(self):
        self.find_by_xpath(Constants.Wizard.HEADER_LINK).click()

    def click_on_download_pdf_button(self):
        self.find_by_xpath(Constants.Wizard.DOWNLOAD_PDF_FILE_BUTTON).click()

    def click_on_close_button(self):
        self.find_by_xpath(Constants.Wizard.CLOSE_WIZARD_BUTTON).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(Constants.Wizard.CANCEL_BUTTON).click()

    def click_on_no_button(self):
        self.find_by_xpath(Constants.Wizard.NO_BUTTON).click()

    def click_on_ok_button(self):
        self.find_by_xpath(Constants.Wizard.OK_BUTTON).click()

    def click_revert_changes_button(self):
        self.find_by_xpath(Constants.Wizard.REVERT_CHANGES_BUTTON).click()

    def click_on_clear_changes_button(self):
        self.find_by_xpath(Constants.Wizard.CLEAR_CHANGES_BUTTON).click()

    def click_on_save_changes_button(self):
        self.find_by_xpath(Constants.Wizard.SAVE_CHANGES_BUTTON).click()

    def is_footer_error_displayed(self):
        return self.is_element_present(Constants.Wizard.FOOTER_ERROR_TEXT)

    def get_footer_error_text(self):
        return self.find_by_xpath(Constants.Wizard.FOOTER_ERROR_TEXT).text


class ValuesTab(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_user_list_name(self, value):
        self.set_text_by_xpath(Constants.ValuesTab.USER_LIST_NAME, value)

    def set_user_list_description(self, value):
        self.set_text_by_xpath(Constants.ValuesTab.USER_LIST_DESCRIPTION, value)

    def click_on_plus_button(self):
        self.find_by_xpath(Constants.ValuesTab.PLUS_BUTTON).click()

    def click_on_save_checkmark_button(self):
        self.find_by_xpath(Constants.ValuesTab.SAVE_CHECKMARK_BUTTON).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(Constants.ValuesTab.CANCEL_BUTTON).click()

    def click_on_edit_button(self):
        self.find_by_xpath(Constants.ValuesTab.EDIT_BUTTON).click()

    def click_on_delete_button(self):
        self.find_by_xpath(Constants.ValuesTab.DELETE_BUTTON).click()

    def set_user_filter(self, value):
        self.set_text_by_xpath(Constants.ValuesTab.USER_FILTER, value)

    def set_user(self, value):
        self.set_combobox_value(Constants.ValuesTab.USER, value)
