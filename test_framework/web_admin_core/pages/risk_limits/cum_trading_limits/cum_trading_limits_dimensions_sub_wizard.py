from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_constants import \
    CumTradingLimitsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class CumTradingLimitsDimensionsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_venue(self, value):
        self.set_combobox_value(CumTradingLimitsConstants.DIMENSIONS_TAB_VENUE_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.DIMENSIONS_TAB_VENUE_XPATH)

    def is_venue_field_displayed(self):
        return self.is_element_present(CumTradingLimitsConstants.DIMENSIONS_TAB_VENUE_XPATH)

    def set_sub_venue(self, value):
        self.set_combobox_value(CumTradingLimitsConstants.DIMENSIONS_TAB_SUB_VENUE_XPATH, value)

    def get_sub_venue(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.DIMENSIONS_TAB_SUB_VENUE_XPATH)

    def is_sub_venue_field_displayed(self):
        return self.is_element_present(CumTradingLimitsConstants.DIMENSIONS_TAB_SUB_VENUE_XPATH)

    def set_listing_group(self, value):
        self.set_combobox_value(CumTradingLimitsConstants.DIMENSIONS_TAB_LISTING_GROUP_XPATH, value)

    def get_listing_group(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.DIMENSIONS_TAB_LISTING_GROUP_XPATH)

    def is_listing_group_field_displayed(self):
        return self.is_element_present(CumTradingLimitsConstants.DIMENSIONS_TAB_LISTING_GROUP_XPATH)

    def set_listing(self, value):
        self.set_combobox_value(CumTradingLimitsConstants.DIMENSIONS_TAB_LISTING_XPATH, value)

    def get_listing(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.DIMENSIONS_TAB_LISTING_XPATH)

    def is_listing_field_displayed(self):
        return self.is_element_present(CumTradingLimitsConstants.DIMENSIONS_TAB_LISTING_XPATH)

    def click_on_per_listing(self):
        self.find_by_xpath(CumTradingLimitsConstants.DIMENSIONS_TAB_PER_LISTING_CHECKBOX_XPATH).click()

    def set_user(self, value):
        self.set_combobox_value(CumTradingLimitsConstants.DIMENSIONS_TAB_USER_XPATH, value)

    def get_user(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.DIMENSIONS_TAB_USER_XPATH)

    def is_user_field_displayed(self):
        return self.is_element_present(CumTradingLimitsConstants.DIMENSIONS_TAB_USER_XPATH)

    def set_desk(self, value):
        self.set_combobox_value(CumTradingLimitsConstants.DIMENSIONS_TAB_DESK_XPATH, value)

    def get_desk(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.DIMENSIONS_TAB_DESK_XPATH)

    def is_desk_field_displayed(self):
        return self.is_element_present(CumTradingLimitsConstants.DIMENSIONS_TAB_DESK_XPATH)

    def set_route(self, value):
        self.set_combobox_value(CumTradingLimitsConstants.DIMENSIONS_TAB_ROUTE_XPATH, value)

    def get_route(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.DIMENSIONS_TAB_ROUTE_XPATH)

    def is_route_field_displayed(self):
        return self.is_element_present(CumTradingLimitsConstants.DIMENSIONS_TAB_ROUTE_XPATH)

    def set_instrument_type(self, value):
        self.set_combobox_value(CumTradingLimitsConstants.DIMENSIONS_TAB_INSTRUMENT_TYPE_XPATH, value)

    def get_instrument_type(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.DIMENSIONS_TAB_INSTRUMENT_TYPE_XPATH)

    def is_instrument_type_field_displayed(self):
        return self.is_element_present(CumTradingLimitsConstants.DIMENSIONS_TAB_INSTRUMENT_TYPE_XPATH)

    def set_client(self, value):
        self.set_combobox_value(CumTradingLimitsConstants.DIMENSIONS_TAB_CLIENT_XPATH, value)

    def get_client(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.DIMENSIONS_TAB_CLIENT_XPATH)

    def is_client_field_displayed(self):
        return self.is_element_present(CumTradingLimitsConstants.DIMENSIONS_TAB_CLIENT_XPATH)

    def set_client_group(self, value):
        self.set_combobox_value(CumTradingLimitsConstants.DIMENSIONS_TAB_CLIENT_GROUP_XPATH, value)

    def get_client_group(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.DIMENSIONS_TAB_CLIENT_GROUP_XPATH)

    def is_client_group_field_displayed(self):
        return self.is_element_present(CumTradingLimitsConstants.DIMENSIONS_TAB_CLIENT_GROUP_XPATH)

    def set_account(self, value):
        self.set_combobox_value(CumTradingLimitsConstants.DIMENSIONS_TAB_ACCOUNT_XPATH, value)

    def get_account(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.DIMENSIONS_TAB_ACCOUNT_XPATH)

    def is_account_field_displayed(self):
        return self.is_element_present(CumTradingLimitsConstants.DIMENSIONS_TAB_ACCOUNT_XPATH)

    def set_instr_symbol(self, value):
        self.set_combobox_value(CumTradingLimitsConstants.DIMENSIONS_TAB_INSTR_SYMBOL_XPATH, value)

    def get_instr_symbol(self):
        return self.get_text_by_xpath(CumTradingLimitsConstants.DIMENSIONS_TAB_INSTR_SYMBOL_XPATH)

    def is_instr_symbol_field_displayed(self):
        return self.is_element_present(CumTradingLimitsConstants.DIMENSIONS_TAB_INSTR_SYMBOL_XPATH)
