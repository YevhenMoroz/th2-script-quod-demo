import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.users.users.users_constants import UsersConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class UsersWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_logout_button(self):
        self.find_by_xpath(UsersConstants.USER_ICON_AT_RIGHT_CORNER).click()
        self.find_by_xpath(UsersConstants.LOGOUT_BUTTON_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(UsersConstants.SAVE_CHANGES_BUTTON).click()

    def click_on_clear_changes(self):
        self.find_by_xpath(UsersConstants.CLEAR_CHANGES_BUTTON).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(UsersConstants.DOWNLOAD_PDF_AT_WIZARD_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def get_incorrect_or_missing_values_exception(self):
        if self.find_by_xpath(
                    UsersConstants.INCORRECT_OR_MISSING_VALUES_EXCEPTION).text == "Incorrect or missing values":
            return True
        else:
            return False
