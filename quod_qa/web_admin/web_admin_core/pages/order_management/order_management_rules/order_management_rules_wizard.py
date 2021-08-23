import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_constants import \
    OrderManagementRulesConstants

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class OrderManagementRulesWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_save_changes(self):
        self.find_by_xpath(OrderManagementRulesConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(OrderManagementRulesConstants.REVERT_CHANGES_XPATH).click()

    def click_on_close_page(self, confirmation):
        self.find_by_xpath(OrderManagementRulesConstants.CLOSE_WIZARD_XPATH).click()
        time.sleep(2)
        if confirmation:
            self.find_by_xpath(OrderManagementRulesConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(OrderManagementRulesConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(OrderManagementRulesConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def is_incorrect_or_missing_value_message_displayed(self):
        if self.find_by_xpath(
                OrderManagementRulesConstants.INCORRECT_OR_MISSING_VALUES_XPATH).text == "Incorrect or missing values":
            return True
        else:
            return False

    def no_results_has_added_message_displayed(self):
        if self.find_by_xpath(
                OrderManagementRulesConstants.NO_RESULTS_HAVE_ADDED_XPATH).text == "No results have added":
            return True
        else:
            return False

    def such_record_already_exists(self):
        if self.find_by_xpath(
                OrderManagementRulesConstants.SUCH_RECORD_ALREADY_EXISTS).text == "Such a record already exists":
            return True
        else:
            return False

    def can_not_contain_more_than_10_conditions_message(self):
        if self.find_by_xpath(
                OrderManagementRulesConstants.CAN_NOT_CONTAIN_MORE_THAN_10_CONDITIONS).text == "Can not contain more than 10 conditions":
            return True
        else:
            return False

    def total_percentage_is_greater_than_100_message(self):
        if self.find_by_xpath(
                OrderManagementRulesConstants.TOTAL_PERCENTAGE_IS_GREATER_THAN_100).text == "Total percentage is greater than 100":
            return True
        else:
            return False
