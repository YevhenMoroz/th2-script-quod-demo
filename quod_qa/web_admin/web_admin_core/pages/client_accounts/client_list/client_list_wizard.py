import time

from quod_qa.web_admin.web_admin_core.pages.client_accounts.client_list.client_list_constants import ClientListConstants
from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientListWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close_wizard(self):
        self.find_by_xpath(ClientListConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(ClientListConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(ClientListConstants.REVERT_CHANGES_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(ClientListConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_go_back_button(self):
        self.find_by_xpath(ClientListConstants.GO_BACK_BUTTON_XPATH).click()

    def set_client_list_name(self, value):
        self.set_text_by_xpath(ClientListConstants.WIZARD_CLIENT_LIST_NAME_XPATH, value)

    def get_client_list_name(self):
        return self.get_text_by_xpath(ClientListConstants.WIZARD_CLIENT_LIST_NAME_XPATH)

    def set_client_list_description(self, value):
        self.set_text_by_xpath(ClientListConstants.WIZARD_CLIENT_LIST_DESCRIPTION_XPATH, value)

    def get_client_list_description(self):
        return self.get_text_by_xpath(ClientListConstants.WIZARD_CLIENT_LIST_DESCRIPTION_XPATH)

    def click_on_plus(self):
        self.find_by_xpath(ClientListConstants.WIZARD_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(ClientListConstants.WIZARD_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(ClientListConstants.WIZARD_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ClientListConstants.WIZARD_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(ClientListConstants.WIZARD_DELETE_BUTTON_XPATH).click()

    def set_client(self, value):
        self.set_combobox_value(ClientListConstants.WIZARD_CLIENT_XPATH, value)

    def get_client(self):
        return self.get_text_by_xpath(ClientListConstants.WIZARD_CLIENT_XPATH)

    def set_client_filter(self, value):
        self.set_text_by_xpath(ClientListConstants.WIZARD_CLIENT_FILTER_XPATH, value)
