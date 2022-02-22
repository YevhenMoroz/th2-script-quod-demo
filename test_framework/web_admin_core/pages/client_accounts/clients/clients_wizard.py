import time

from test_framework.web_admin_core.pages.client_accounts.clients.clients_constants import ClientsConstants
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientsWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(ClientsConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(ClientsConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(ClientsConstants.REVERT_CHANGES_XPATH).click()

    def click_on_go_back(self):
        self.find_by_xpath(ClientsConstants.GO_BACK_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(ClientsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def is_incorrect_or_missing_value_message_displayed(self):
        if self.find_by_xpath(
                ClientsConstants.INCORRECT_OR_MISSING_VALUES_MESSAGE_XPATH).text == "Incorrect or missing values":
            return True
        else:
            return False

    def is_request_failed_message_displayed(self):
        if self.find_by_xpath(
                ClientsConstants.REQUEST_FAILED_MESSAGE_XPATH).text == "Request failed, verify the input data. " \
                                                                                    "If the problem persists, " \
                                                                                    "please contact the administrator " \
                                                                                    "for full details":
            return True
        else:
            return False
