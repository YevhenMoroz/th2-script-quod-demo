from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.risk_limits.position_limits.position_limits_constants import \
    PositionsLimitsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class PositionLimitsDimensionsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_instrument(self, value):
        self.set_text_by_xpath(PositionsLimitsConstants.DIMENSIONS_TAB_INSTRUMENT_XPATH, value)

    def get_instrument(self):
        return self.get_text_by_xpath(PositionsLimitsConstants.DIMENSIONS_TAB_INSTRUMENT_XPATH)

    def is_instrument_field_displayed(self):
        return self.is_element_present(PositionsLimitsConstants.DIMENSIONS_TAB_INSTRUMENT_XPATH)

    def set_instrument_group(self, value):
        self.set_combobox_value(PositionsLimitsConstants.DIMENSIONS_TAB_INSTRUMENT_GROUP_XPATH, value)

    def get_instrument_group(self):
        return self.get_text_by_xpath(PositionsLimitsConstants.DIMENSIONS_TAB_INSTRUMENT_GROUP_XPATH)

    def is_instrument_group_field_displayed(self):
        return self.is_element_present(PositionsLimitsConstants.DIMENSIONS_TAB_INSTRUMENT_GROUP_XPATH)

    def set_instrument_type(self, value):
        self.set_combobox_value(PositionsLimitsConstants.DIMENSIONS_TAB_INSTRUMENT_TYPE_XPATH, value)

    def get_instrument_type(self):
        return self.get_text_by_xpath(PositionsLimitsConstants.DIMENSIONS_TAB_INSTRUMENT_TYPE_XPATH)

    def is_instrument_type_field_displayed(self):
        return self.is_element_present(PositionsLimitsConstants.DIMENSIONS_TAB_INSTRUMENT_TYPE_XPATH)

    def set_account(self, value):
        self.set_combobox_value(PositionsLimitsConstants.DIMENSIONS_TAB_ACCOUNT_XPATH, value)

    def get_account(self):
        return self.get_text_by_xpath(PositionsLimitsConstants.DIMENSIONS_TAB_ACCOUNT_XPATH)

    def is_account_type_field_displayed(self):
        return self.is_element_present(PositionsLimitsConstants.DIMENSIONS_TAB_ACCOUNT_XPATH)

    def click_on_per_instrument_checkbox(self):
        self.find_by_xpath(PositionsLimitsConstants.DIMENSIONS_TAB_PER_INSTRUMENT_CHECKBOX_XPATH).click()

    def click_on_per_instr_type_checkbox(self):
        self.find_by_xpath(PositionsLimitsConstants.DIMENSIONS_TAB_PER_INSTR_TYPE_CHECKBOX_XPATH).click()

    def click_on_per_instr_group_checkbox(self):
        self.find_by_xpath(PositionsLimitsConstants.DIMENSIONS_TAB_PER_INSTR_GROUP_CHECKBOX_XPATH).click()
