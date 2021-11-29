from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.middle_office.fees.fees_constants import FeesConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


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

    def set_instrument_list(self, value):
        self.set_combobox_value(FeesConstants.DIMENSIONS_TAB_INSTRUMENT_LIST_XPATH, value)

    def get_instrument_list(self):
        return self.get_text_by_xpath(FeesConstants.DIMENSIONS_TAB_INSTRUMENT_LIST_XPATH)

    def set_instrument_group(self, value):
        self.set_combobox_value(FeesConstants.DIMENSIONS_TAB_INSTRUMENT_GROUP_XPATH, value)

    def get_instrument_group(self):
        return self.get_text_by_xpath(FeesConstants.DIMENSIONS_TAB_INSTRUMENT_GROUP_XPATH)
