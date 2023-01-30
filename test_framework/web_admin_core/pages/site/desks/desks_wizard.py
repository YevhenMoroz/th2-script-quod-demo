import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.site.desks.desks_constants import DesksConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class DesksWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_save_changes(self):
        self.find_by_xpath(DesksConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(DesksConstants.REVERT_CHANGES_BUTTON_XPATH).click()

    def click_on_close_wizard(self):
        self.find_by_xpath(DesksConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_ok_button(self):
        self.find_by_xpath(DesksConstants.OK_BUTTON_XPATH).click()

    def click_on_no_button(self):
        self.find_by_xpath(DesksConstants.NO_BUTTON_XPATH).click()

    def click_on_cancel(self):
        self.find_by_xpath(DesksConstants.CANCEL_BUTTON_XPATH).click()

    def is_incorrect_or_missing_value_message_displayed(self):
        return True if self.find_by_xpath(
                DesksConstants.INCORRECT_OR_MISSING_VALUES_MESSAGE_XPATH).text == "Incorrect or missing values" \
            else False

    def is_leave_page_confirmation_pop_up_displayed(self):
        return self.is_element_present(DesksConstants.CONFIRMATION_POP_UP)
