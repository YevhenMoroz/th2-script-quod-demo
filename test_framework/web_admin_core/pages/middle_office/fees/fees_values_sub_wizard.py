import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_constants import FeesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class FeesValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_description(self, value):
        self.set_text_by_xpath(FeesConstants.VALUES_TAB_DESCRIPTION_XPATH, value)

    def set_misc_fee_type(self, value):
        self.select_value_from_dropdown_list(FeesConstants.VALUES_TAB_MISC_FEE_TYPE_XPATH, value)

    def get_misc_fee_type(self):
        return self.get_text_by_xpath(FeesConstants.VALUES_TAB_MISC_FEE_TYPE_XPATH)

    def get_all_misc_fee_type_from_drop_menu(self):
        self.find_by_xpath(FeesConstants.VALUES_TAB_MISC_FEE_TYPE_XPATH).click()
        time.sleep(1)
        items = self.get_all_items_from_drop_down(FeesConstants.DROP_DOWN_MENU_XPATH)
        self.find_by_xpath(FeesConstants.VALUES_TAB_MISC_FEE_TYPE_XPATH).click()
        return items

    def set_charge_type(self, value):
        self.select_value_from_dropdown_list(FeesConstants.VALUES_TAB_CHARGE_TYPE_XPATH, value)

    def get_charge_type(self):
        return self.get_text_by_xpath(FeesConstants.VALUES_TAB_CHARGE_TYPE_XPATH)

    def set_order_scope(self, value):
        self.select_value_from_dropdown_list(FeesConstants.VALUES_TAB_ORDER_SCOPE_XPATH, value)

    def get_order_scope(self):
        return self.get_text_by_xpath(FeesConstants.VALUES_TAB_ORDER_SCOPE_XPATH)

    def set_order_fee_profile(self, value):
        self.set_combobox_value(FeesConstants.VALUES_TAB_ORDER_FEE_PROFILE_XPATH, value)

    def get_order_fee_profile(self):
        return self.get_text_by_xpath(FeesConstants.VALUES_TAB_ORDER_FEE_PROFILE_XPATH)

    def set_exec_scope(self, value):
        self.select_value_from_dropdown_list(FeesConstants.VALUES_TAB_EXEC_SCOPE_XPATH, value)

    def get_exec_scope(self):
        return self.get_text_by_xpath(FeesConstants.VALUES_TAB_EXEC_SCOPE_XPATH)

    def set_exec_fee_profile(self, value):
        self.set_combobox_value(FeesConstants.VALUES_TAB_EXEC_FEE_PROFILE_XPATH, value)

    def get_exec_fee_profile(self):
        return self.get_text_by_xpath(FeesConstants.VALUES_TAB_EXEC_FEE_PROFILE_XPATH)

    def set_re_calculate_for_allocations(self):
        self.find_by_xpath(FeesConstants.VALUES_TAB_RE_CALCULATE_FOR_ALLOCATIONS_CHECKBOX).click()

    def click_on_manage_order_fee_profile(self):
        self.find_by_xpath(FeesConstants.VALUES_TAB_MANAGE_ORDER_FEE_PROFILE).click()

    def click_on_manage_exec_fee_profile(self):
        self.find_by_xpath(FeesConstants.VALUES_TAB_MANAGE_EXEC_FEE_PROFILE).click()
