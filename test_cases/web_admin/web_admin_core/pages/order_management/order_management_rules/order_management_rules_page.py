import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_constants import \
    OrderManagementRulesConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class OrderManagementRulesPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # change criteria
    def click_on_change_criteria(self):
        self.find_by_xpath(OrderManagementRulesConstants.CHANGE_CRITERIA_AT_MAIN_MENU_XPATH).click()

    def click_on_change_criteria_for_saving(self, confirmation):
        self.find_by_xpath(OrderManagementRulesConstants.SAVE_CHANGE_CRITERIA_AT_MAIN_MENU_XPATH).click()
        time.sleep(2)
        try:
            if confirmation:
                self.find_by_xpath(OrderManagementRulesConstants.OK_BUTTON_XPATH).click()
            else:
                self.find_by_xpath(OrderManagementRulesConstants.CANCEL_BUTTON_XPATH).click()
        except Exception:
            return

    def set_first_criteria(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.FIRST_CRITERIA_FIELD_AT_CHANGE_CRITERIA_TAB_XPATH, value)

    def set_second_criteria(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.SECOND_CRITERIA_FIELD_AT_CHANGE_CRITERIA_TAB_XPATH, value)

    def set_third_criteria(self, value):
        self.set_combobox_value(OrderManagementRulesConstants.THIRD_CRITERIA_FIELD_AT_CHANGE_CRITERIA_TAB_XPATH, value)

    # left menu
    def click_on_enabled_disable(self, confirmation):
        self.find_by_xpath(OrderManagementRulesConstants.ENABLE_DISABLE_BUTTON_XPATH).click()
        time.sleep(2)
        if confirmation:
            self.find_by_xpath(OrderManagementRulesConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(OrderManagementRulesConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_more_actions(self):
        self.find_by_xpath(OrderManagementRulesConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit_at_more_actions(self):
        self.find_by_xpath(OrderManagementRulesConstants.EDIT_XPATH).click()

    def click_on_clone_at_more_actions(self):
        self.find_by_xpath(OrderManagementRulesConstants.CLONE_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value: str):
        self.clear_download_directory()
        self.find_by_xpath(OrderManagementRulesConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row_at_more_actions(self):
        self.find_by_xpath(OrderManagementRulesConstants.PIN_ROW_XPATH).click()

    def click_on_ok_button(self):
        self.find_by_xpath(OrderManagementRulesConstants.OK_BUTTON_XPATH).click()

    # -------------
    def click_on_new_button(self):
        self.find_by_xpath(OrderManagementRulesConstants.NEW_BUTTON_XPATH).click()
        time.sleep(1)

    def set_name_filter(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def set_enabled_filter(self, value):
        self.select_value_from_dropdown_list(OrderManagementRulesConstants.MAIN_PAGE_ENABLED_FILTER_LIST_XPATH.format(value))

    def set_listing_group_filter(self, value):
        self.set_text_by_xpath(OrderManagementRulesConstants.MAIN_PAGE_LISTING_GROUP_FILTER_XPATH, value)

    def click_on_enabled_field(self):
        self.find_by_xpath(OrderManagementRulesConstants.MAIN_PAGE_ENABLED_FILTER_XPATH).click()
        time.sleep(2)