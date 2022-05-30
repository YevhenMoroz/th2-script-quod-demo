import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_constants import FeesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class FeesDimensionsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_instr_type(self, value):
        self.set_combobox_value(FeesConstants.DIMENSIONS_TAB_INSTR_TYPE_XPATH, value)

    def get_instr_type(self):
        return self.get_text_by_xpath(FeesConstants.DIMENSIONS_TAB_INSTR_TYPE_XPATH)

    def set_side(self, value):
        self.set_combobox_value(FeesConstants.DIMENSIONS_TAB_SIDE_XPATH, value)

    def get_side(self):
        return self.get_text_by_xpath(FeesConstants.DIMENSIONS_TAB_SIDE_XPATH)

    def set_country_of_issue(self, value):
        self.set_combobox_value(FeesConstants.DIMENSIONS_TAB_COUNTRY_OF_ISSUE_XPATH, value)

    def get_country_of_issue(self):
        return self.get_text_by_xpath(FeesConstants.DIMENSIONS_TAB_COUNTRY_OF_ISSUE_XPATH)

    def set_venue(self, value):
        self.set_combobox_value(FeesConstants.DIMENSIONS_TAB_VENUE_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(FeesConstants.DIMENSIONS_TAB_VENUE_XPATH)

    def is_venue_field_enable(self):
        return self.is_field_enabled(FeesConstants.DIMENSIONS_TAB_VENUE_XPATH)

    def get_all_venue_from_drop_menu(self):
        self.find_by_xpath(FeesConstants.DIMENSIONS_TAB_VENUE_XPATH).click()
        time.sleep(2)
        return self._get_all_items_from_drop_down(FeesConstants.DIMENSIONS_TAB_DROP_DOWN_MENU_ITEMS_XPATH)

    def set_venue_list(self, value):
        self.set_combobox_value(FeesConstants.DIMENSIONS_TAB_VENUE_LIST_XPATH, value)

    def get_venue_list(self):
        return self.get_text_by_xpath(FeesConstants.DIMENSIONS_TAB_VENUE_LIST_XPATH)

    def is_venue_list_field_enable(self):
        return self.is_field_enabled(FeesConstants.DIMENSIONS_TAB_VENUE_LIST_XPATH)

    def get_all_venue_list_from_drop_menu(self):
        self.find_by_xpath(FeesConstants.DIMENSIONS_TAB_VENUE_LIST_XPATH).click()
        time.sleep(2)
        return self._get_all_items_from_drop_down(FeesConstants.DIMENSIONS_TAB_DROP_DOWN_MENU_ITEMS_XPATH)

    def set_instrument_list(self, value):
        self.set_combobox_value(FeesConstants.DIMENSIONS_TAB_INSTRUMENT_LIST_XPATH, value)

    def get_instrument_list(self):
        return self.get_text_by_xpath(FeesConstants.DIMENSIONS_TAB_INSTRUMENT_LIST_XPATH)

    def set_instrument_group(self, value):
        self.set_combobox_value(FeesConstants.DIMENSIONS_TAB_INSTRUMENT_GROUP_XPATH, value)

    def get_instrument_group(self):
        return self.get_text_by_xpath(FeesConstants.DIMENSIONS_TAB_INSTRUMENT_GROUP_XPATH)
