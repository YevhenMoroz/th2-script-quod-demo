import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.users.users.users_constants import UsersConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class UsersWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_logout_button(self):
        self.find_by_xpath(UsersConstants.USER_ICON_AT_RIGHT_CORNER).click()
        self.find_by_xpath(UsersConstants.LOGOUT_BUTTON_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(UsersConstants.SAVE_CHANGES_BUTTON).click()

    def click_on_clear_changes(self):
        self.find_by_xpath(UsersConstants.REVERT_CHANGES_BUTTON).click()

    def is_revert_changes_button_enabled(self):
        return self.find_by_xpath(UsersConstants.REVERT_CHANGES_BUTTON).is_enabled()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(UsersConstants.DOWNLOAD_PDF_AT_WIZARD_XPATH).click()
        time.sleep(3)
        return self.is_pdf_contains_value(value)

    def get_incorrect_or_missing_values_exception(self):
        if self.find_by_xpath(
                    UsersConstants.INCORRECT_OR_MISSING_VALUES_EXCEPTION).text == "Incorrect or missing values":
            return True
        else:
            return False

    def is_warning_displayed(self):
        return True if self.is_element_present(UsersConstants.WARNING_MESSAGE) else False

    def is_request_failed_message_displayed(self):
        return self.find_by_xpath(UsersConstants.REQUEST_FAILED_MESSAGE_XPATH).is_displayed()

    def is_online_status_displayed(self):
        return self.is_element_present(UsersConstants.ONLINE_STATUS_XPATH)

    def is_confirmation_pop_displayed(self):
        return self.is_element_present(UsersConstants.CONFIRM_POP_UP)

    def accept_or_cancel_confirmation(self, confirm: bool):
        self.find_by_xpath(UsersConstants.OK_BUTTON_XPATH).click() if confirm \
            else self.find_by_xpath(UsersConstants.CANCEL_BUTTON_XPATH).click()


