from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.risk_limits.trading_limits.trading_limits_constants import \
    TradingLimitsConstants

from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class TradingLimitsDimensionsSubWizardPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_venue(self, value):
        self.set_combobox_value(TradingLimitsConstants.DIMENSIONS_TAB_VENUE_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(TradingLimitsConstants.DIMENSIONS_TAB_VENUE_XPATH)

    def set_sub_venue(self, value):
        self.set_combobox_value(TradingLimitsConstants.DIMENSIONS_TAB_SUB_VENUE_XPATH, value)

    def get_sub_venue(self):
        return self.get_text_by_xpath(TradingLimitsConstants.DIMENSIONS_TAB_SUB_VENUE_XPATH)

    def set_listing_group(self, value):
        self.set_combobox_value(TradingLimitsConstants.DIMENSIONS_TAB_LISTING_GROUP_XPATH, value)

    def get_listing_group(self):
        return self.get_text_by_xpath(TradingLimitsConstants.DIMENSIONS_TAB_LISTING_GROUP_XPATH)

    def set_user(self, value):
        self.set_combobox_value(TradingLimitsConstants.DIMENSIONS_TAB_USER_XPATH, value)

    def get_user(self):
        return self.get_text_by_xpath(TradingLimitsConstants.DIMENSIONS_TAB_USER_XPATH)

    def set_client(self, value):
        self.set_combobox_value(TradingLimitsConstants.DIMENSIONS_TAB_CLIENT_XPATH, value)

    def get_client(self):
        return self.get_text_by_xpath(TradingLimitsConstants.DIMENSIONS_TAB_CLIENT_XPATH)

    def set_client_group(self, value):
        self.set_combobox_value(TradingLimitsConstants.DIMENSIONS_TAB_CLIENT_GROUP_XPATH, value)

    def get_client_group(self):
        return self.get_text_by_xpath(TradingLimitsConstants.DIMENSIONS_TAB_CLIENT_GROUP_XPATH)

    def set_desk(self, value):
        self.set_combobox_value(TradingLimitsConstants.DIMENSIONS_TAB_DESK_XPATH, value)

    def get_desk(self):
        return self.get_text_by_xpath(TradingLimitsConstants.DIMENSIONS_TAB_DESK_XPATH)

    def set_route(self, value):
        self.set_combobox_value(TradingLimitsConstants.DIMENSIONS_TAB_ROUTE_XPATH, value)

    def get_route(self):
        return self.get_text_by_xpath(TradingLimitsConstants.DIMENSIONS_TAB_ROUTE_XPATH)

    def set_instrument_type(self, value):
        self.set_combobox_value(TradingLimitsConstants.DIMENSIONS_TAB_INSTRUMENT_TYPE_XPATH, value)

    def get_instrument_type(self):
        return self.get_text_by_xpath(TradingLimitsConstants.DIMENSIONS_TAB_INSTRUMENT_TYPE_XPATH)

    def set_instr_symbol(self, value):
        self.set_combobox_value(TradingLimitsConstants.DIMENSIONS_TAB_INSTR_SYMBOL_XPATH, value)

    def get_instr_symbol(self):
        return self.get_text_by_xpath(TradingLimitsConstants.DIMENSIONS_TAB_INSTR_SYMBOL_XPATH)

    def set_execution_policy(self, value):
        self.set_combobox_value(TradingLimitsConstants.DIMENSIONS_TAB_EXECUTION_POLICY_XPATH, value)

    def get_execution_policy(self):
        return self.get_text_by_xpath(TradingLimitsConstants.DIMENSIONS_TAB_EXECUTION_POLICY_XPATH)

    def set_phase(self, value):
        self.set_combobox_value(TradingLimitsConstants.DIMENSIONS_TAB_PHASE_XPATH, value)

    def get_phase(self):
        return self.get_text_by_xpath(TradingLimitsConstants.DIMENSIONS_TAB_PHASE_XPATH)
