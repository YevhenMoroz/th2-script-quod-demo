import time

from test_framework.web_admin_core.pages.client_accounts.external_client_groups_ids.constants import \
    ExternalClientGroupIDsConstants
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ExternalClientGroupIDsWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close_wizard(self):
        self.find_by_xpath(ExternalClientGroupIDsConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(ExternalClientGroupIDsConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(ExternalClientGroupIDsConstants.REVERT_CHANGES_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(ExternalClientGroupIDsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_go_back_button(self):
        self.find_by_xpath(ExternalClientGroupIDsConstants.GO_BACK_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(ExternalClientGroupIDsConstants.WIZARD_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(ExternalClientGroupIDsConstants.WIZARD_NAME_XPATH)

    def set_client_group(self, value):
        self.set_combobox_value(ExternalClientGroupIDsConstants.WIZARD_CLIENT_GROUP_XPATH, value)

    def get_client_group(self):
        self.get_text_by_xpath(ExternalClientGroupIDsConstants.WIZARD_CLIENT_GROUP_XPATH)
