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

    def set_venue_list(self, value):
        self.set_combobox_value(CommissionsConstants.VALUES_TAB_VENUE_LIST_XPATH, value)

    def get_venue_list(self):
        return self.get_text_by_xpath(CommissionsConstants.VALUES_TAB_VENUE_LIST_XPATH)

    def get_all_venue_list_from_drop_menu(self):
        self.find_by_xpath(CommissionsConstants.VALUES_TAB_VENUE_LIST_XPATH).click()
        time.sleep(2)
        return self.get_all_items_from_drop_down(CommissionsConstants.DROP_DOWN_MENU_XPATH)
