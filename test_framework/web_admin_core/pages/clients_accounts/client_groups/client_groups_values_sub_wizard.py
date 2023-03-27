import time
from test_framework.web_admin_core.pages.clients_accounts.client_groups.client_groups_constants import \
    ClientGroupsConstants
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientGroupsValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(ClientGroupsConstants.VALUES_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(ClientGroupsConstants.VALUES_TAB_NAME_XPATH)

    def set_description(self, value):
        self.set_text_by_xpath(ClientGroupsConstants.VALUES_TAB_DESCRIPTION_XPATH, value)

    def get_description(self):
        return self.get_text_by_xpath(ClientGroupsConstants.VALUES_TAB_DESCRIPTION_XPATH)

    def set_self_help_behavior(self, value):
        self.set_combobox_value(ClientGroupsConstants.VALUES_TAB_SELF_HELP_BEHAVIOR_XPATH, value)

    def get_self_help_behavior(self):
        self.get_text_by_xpath(ClientGroupsConstants.VALUES_TAB_SELF_HELP_BEHAVIOR_XPATH)

    def set_confirmation_service(self, value):
        self.select_value_from_dropdown_list(ClientGroupsConstants.VALUES_TAB_CONFIRMATION_SERVICE_XPATH, value)

    def get_confirmation_service(self):
        return self.get_text_by_xpath(ClientGroupsConstants.VALUES_TAB_CONFIRMATION_SERVICE_XPATH)

    def get_all_confirmation_service_from_drop_menu(self):
        self.find_by_xpath(ClientGroupsConstants.VALUES_TAB_CONFIRMATION_SERVICE_XPATH).click()
        time.sleep(1)
        items = self.get_all_items_from_drop_down(ClientGroupsConstants.DROP_DOWN_MENU_XPATH)
        self.find_by_xpath(ClientGroupsConstants.VALUES_TAB_CONFIRMATION_SERVICE_XPATH).click()
        return items

    def set_block_approval(self, value):
        self.select_value_from_dropdown_list(ClientGroupsConstants.VALUES_TAB_BLOCK_APPROVAL_XPATH, value)

    def get_block_approval(self):
        return self.get_text_by_xpath(ClientGroupsConstants.VALUES_TAB_BLOCK_APPROVAL_XPATH)

    def get_all_block_approval_from_drop_menu(self):
        self.find_by_xpath(ClientGroupsConstants.VALUES_TAB_BLOCK_APPROVAL_XPATH).click()
        time.sleep(1)
        items = self.get_all_items_from_drop_down(ClientGroupsConstants.DROP_DOWN_MENU_XPATH)
        self.find_by_xpath(ClientGroupsConstants.VALUES_TAB_BLOCK_APPROVAL_XPATH).click()
        return items

    def set_user_manager(self, value):
        self.set_combobox_value(ClientGroupsConstants.VALUES_TAB_USER_MANAGER_XPATH, value)

    def get_user_manager(self):
        return self.get_text_by_xpath(ClientGroupsConstants.VALUES_TAB_USER_MANAGER_XPATH)

    def get_all_user_manager_from_drop_menu(self):
        self.set_text_by_xpath(ClientGroupsConstants.VALUES_TAB_USER_MANAGER_XPATH, "")
        time.sleep(1)
        return self.get_all_items_from_drop_down(ClientGroupsConstants.DROP_DOWN_MENU_XPATH)

    def set_booking_inst(self, value):
        self.set_combobox_value(ClientGroupsConstants.VALUES_TAB_BOOKING_INST_XPATH, value)

    def get_booking_inst(self):
        return self.get_text_by_xpath(ClientGroupsConstants.VALUES_TAB_BOOKING_INST_XPATH)

    def set_allocation_inst(self, value):
        self.set_combobox_value(ClientGroupsConstants.VALUES_TAB_ALLOCATION_INST_XPATH, value)

    def get_allocation(self):
        return self.get_text_by_xpath(ClientGroupsConstants.VALUES_TAB_ALLOCATION_INST_XPATH)

    def set_rounding_direction(self, value):
        self.set_combobox_value(ClientGroupsConstants.VALUES_TAB_ROUNDING_DIRECTION_XPATH, value)

    def get_rounding_direction(self):
        return self.get_text_by_xpath(ClientGroupsConstants.VALUES_TAB_ROUNDING_DIRECTION_XPATH)

    def set_price_precision(self, value):
        self.set_text_by_xpath(ClientGroupsConstants.VALUES_TAB_PRICE_PRECISION_XPATH, value)

    def get_price_precision(self):
        return self.get_text_by_xpath(ClientGroupsConstants.VALUES_TAB_PRICE_PRECISION_XPATH)
