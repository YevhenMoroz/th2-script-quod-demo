import time
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_constants import CommissionsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class CommissionsValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(CommissionsConstants.VALUES_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(CommissionsConstants.VALUES_TAB_NAME_XPATH)

    def set_description(self, value):
        self.set_text_by_xpath(CommissionsConstants.VALUES_TAB_DESCRIPTION_XPATH, value)

    def get_description(self):
        return self.get_text_by_xpath(CommissionsConstants.VALUES_TAB_DESCRIPTION_XPATH)

    def click_on_re_calculate_for_allocations(self):
        self.find_by_xpath(CommissionsConstants.VALUES_TAB_RE_CALCULATE_FOR_ALLOCATIONS_XPATH).click()

    def is_re_calculate_for_allocations_selected(self):
        return self.is_checkbox_selected(CommissionsConstants.VALUES_TAB_RE_CALCULATE_FOR_ALLOCATIONS_XPATH)

    def set_commission_amount_type(self, value):
        self.set_combobox_value(CommissionsConstants.DIMENSIONS_TAB_COMMISSION_AMOUNT_TYPE_XPATH, value)

    def get_commission_amount_type(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_COMMISSION_AMOUNT_TYPE_XPATH)

    def get_all_commission_amount_type_from_drop_menu(self):
        self.find_by_xpath(CommissionsConstants.DIMENSIONS_TAB_COMMISSION_AMOUNT_TYPE_XPATH).click()
        time.sleep(1)
        return self._get_all_items_from_drop_down(CommissionsConstants.DROP_DOWN_MENU_XPATH)

    def set_commission_profile(self, value):
        self.set_combobox_value(CommissionsConstants.DIMENSIONS_TAB_COMMISSION_PROFILE_XPATH, value)

    def get_commission_profile(self):
        return self.get_text_by_xpath(CommissionsConstants.DIMENSIONS_TAB_COMMISSION_PROFILE_XPATH)

    def get_all_commission_profile_from_drop_menu(self):
        self.find_by_xpath(CommissionsConstants.DIMENSIONS_TAB_COMMISSION_PROFILE_XPATH).click()
        time.sleep(1)
        return self._get_all_items_from_drop_down(CommissionsConstants.DROP_DOWN_MENU_XPATH)

    def click_on_manage_commission_profile(self):
        self.find_by_xpath(CommissionsConstants.DIMENSIONS_TAB_MANAGE_COMMISSION_PROFILE_XPATH).click()

