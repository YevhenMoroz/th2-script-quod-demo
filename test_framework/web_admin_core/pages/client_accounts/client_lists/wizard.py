import time

from test_framework.web_admin_core.pages.client_accounts.client_lists.constants import ClientListsConstants
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientListsWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close_wizard(self):
        self.find_by_xpath(ClientListsConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(ClientListsConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(ClientListsConstants.REVERT_CHANGES_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(ClientListsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_go_back_button(self):
        self.find_by_xpath(ClientListsConstants.GO_BACK_BUTTON_XPATH).click()

    def set_client_list_name(self, value):
        self.set_text_by_xpath(ClientListsConstants.WIZARD_CLIENT_LIST_NAME_XPATH, value)

    def get_client_list_name(self):
        return self.get_text_by_xpath(ClientListsConstants.WIZARD_CLIENT_LIST_NAME_XPATH)

    def set_client_list_description(self, value):
        self.set_text_by_xpath(ClientListsConstants.WIZARD_CLIENT_LIST_DESCRIPTION_XPATH, value)

    def get_client_list_description(self):
        return self.get_text_by_xpath(ClientListsConstants.WIZARD_CLIENT_LIST_DESCRIPTION_XPATH)

    def click_on_plus(self):
        self.find_by_xpath(ClientListsConstants.WIZARD_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(ClientListsConstants.WIZARD_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(ClientListsConstants.WIZARD_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ClientListsConstants.WIZARD_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(ClientListsConstants.WIZARD_DELETE_BUTTON_XPATH).click()

    def set_client(self, value):
        self.set_combobox_value(ClientListsConstants.WIZARD_CLIENT_XPATH, value)

    def get_client(self):
        return self.get_text_by_xpath(ClientListsConstants.WIZARD_CLIENT_XPATH)

    def get_all_client_from_table(self):
        return self._get_all_items_from_table_column(ClientListsConstants.WIZARD_DISPLAYED_CLIENTS_AT_TABLE)

    def set_client_filter(self, value):
        self.set_text_by_xpath(ClientListsConstants.WIZARD_CLIENT_FILTER_XPATH, value)

    def is_should_contain_at_least_one_client_warning_appears(self):
        return "Should contain at least one client" == self.find_by_xpath(ClientListsConstants.WIZARD_WARNING_MESSAGE_TEXT_XPATH).text

    def is_client_list_wizard_opened(self):
        return self.is_element_present(ClientListsConstants.WIZARD_TITLE_CLIENT_LIST_XPATH)

    def click_at_client_link(self):
        self.find_by_xpath(ClientListsConstants.WIZARD_CLIENT_LINK_NAME_XPATH).click()

    def click_on_no_button(self):
        self.find_by_xpath(ClientListsConstants.NO_BUTTON_XPATH).click()

    def click_on_ok_button(self):
        self.find_by_xpath(ClientListsConstants.OK_BUTTON_XPATH).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(ClientListsConstants.CANCEL_BUTTON_XPATH).click()
