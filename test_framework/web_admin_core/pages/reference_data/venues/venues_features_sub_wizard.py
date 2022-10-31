import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.reference_data.venues.venues_constants import VenuesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesFeaturesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_support_public_quote_req(self):
        self.find_by_xpath(VenuesConstants.FEATURES_TAB_SUPPORT_PUBLIC_QUOTE_REQ_CHECKBOX_XPATH).click()

    def is_support_public_quote_req_selected(self):
        return self.find_by_xpath(VenuesConstants.FEATURES_TAB_SUPPORT_PUBLIC_QUOTE_REQ_CHECKBOX_XPATH)

    def set_quote_responce_level(self, value):
        self.set_combobox_value(VenuesConstants.FEATURES_TAB_QUOTE_RESPONCE_LEVEL_XPATH, value)

    def get_quote_responce_level(self):
        return self.get_text_by_xpath(VenuesConstants.FEATURES_TAB_QUOTE_RESPONCE_LEVEL_XPATH)

    def set_multileg_report_type(self, value):
        self.set_combobox_value(VenuesConstants.FEATURES_TAB_MULTILEG_REPORT_TYPE_XPATH, value)

    def get_multileg_report_type(self):
        return self.get_text_by_xpath(VenuesConstants.FEATURES_TAB_QUOTE_RESPONCE_LEVEL_XPATH)

    def set_min_resident_time(self, value):
        self.set_text_by_xpath(VenuesConstants.FEATURES_TAB_MIN_RESIDENT_TIME_XPATH, value)

    def get_min_resident_time(self):
        return self.get_text_by_xpath(VenuesConstants.FEATURES_TAB_MIN_RESIDENT_TIME_XPATH)

    def set_open_time(self, value):
        self.set_text_by_xpath(VenuesConstants.FEATURES_TAB_OPEN_TIME_XPATH, value)

    def get_open_time(self):
        return self.get_text_by_xpath(VenuesConstants.FEATURES_TAB_OPEN_TIME_XPATH)

    def click_on_hold_fix_sell(self):
        self.find_by_xpath(VenuesConstants.FEATURES_TAB_HOLD_FIX_SELL_CHECKBOX_XPATH).click()

    def is_hold_fix_sell_selected(self):
        return self.is_checkbox_selected(VenuesConstants.FEATURES_TAB_HOLD_FIX_SELL_CHECKBOX_XPATH)

    def set_time_zone(self, value):
        self.set_text_by_xpath(VenuesConstants.FEATURES_TAB_TIME_ZONE_XPATH, value)

    def get_time_zone(self):
        return self.get_text_by_xpath(VenuesConstants.FEATURES_TAB_TIME_ZONE_XPATH)

    def get_all_time_zones_from_drop_menu(self):
        self.set_time_zone("")
        time.sleep(1)
        return self.get_all_items_from_drop_down(VenuesConstants.FEATURES_TAB_TIME_ZONE_XPATH)

    def set_default_execution_strategy(self, value):
        self.set_combobox_value(VenuesConstants.FEATURES_TAB_DEFAULT_EXECUTION_STRATEGY_XPATH, value)

    def get_default_execution_strategy(self):
        return self.get_text_by_xpath(VenuesConstants.FEATURES_TAB_TIME_ZONE_XPATH)

    def set_venue_sto(self, value):
        self.set_combobox_value(VenuesConstants.FEATURES_TAB_VENUE_STO_XPATH, value)

    def get_venue_sto(self):
        self.get_text_by_xpath(VenuesConstants.FEATURES_TAB_VENUE_STO_XPATH)

    def click_on_support_reverse_cal_spread(self):
        self.find_by_xpath(VenuesConstants.FEATURES_TAB_SUPPORT_REVERSE_CAL_SPREAD_CHECKBOX_XPATH).click()

    def is_support_reverse_cal_spread_selected(self):
        self.is_checkbox_selected(VenuesConstants.FEATURES_TAB_SUPPORT_REVERSE_CAL_SPREAD_CHECKBOX_XPATH)

    def click_on_gtd_holiday_check(self):
        self.find_by_xpath(VenuesConstants.FEATURES_TAB_GTD_HOLIDAY_CHECK_CHECKBOX_XPATH).click()

    def is_gtd_holiday_check(self):
        return self.is_checkbox_selected(VenuesConstants.FEATURES_TAB_GTD_HOLIDAY_CHECK_CHECKBOX_XPATH)

    def set_instr_creation_policy(self, value):
        self.set_combobox_value(VenuesConstants.FEATURES_TAB_INSTR_CREATION_POLICY_XPATH, value)

    def get_instr_creation_policy(self):
        return self.get_text_by_xpath(VenuesConstants.FEATURES_TAB_INSTR_CREATION_POLICY_XPATH)

    def set_disable_sell_price_fall(self, value):
        self.set_text_by_xpath(VenuesConstants.FEATURES_TAB_DISABLE_SELL_PRICE_FALL_XPATH, value)

    def get_disable_sell_price_fall(self):
        return self.get_text_by_xpath(VenuesConstants.FEATURES_TAB_DISABLE_SELL_PRICE_FALL_XPATH)

    def set_close_time(self, value):
        self.set_text_by_xpath(VenuesConstants.FEATURES_TAB_CLOSE_TIME_XPATH, value)

    def get_close_time(self):
        return self.get_text_by_xpath(VenuesConstants.FEATURES_TAB_CLOSE_TIME_XPATH)

    def click_on_regulated_sell(self):
        self.find_by_xpath(VenuesConstants.FEATURES_TAB_REGULATED_SELL_CHECKBOX_XPATH).click()

    def is_regulated_sell_selected(self):
        return self.is_checkbox_selected(VenuesConstants.FEATURES_TAB_REGULATED_SELL_CHECKBOX_XPATH)

    def click_on_validate_venue_act_grp_name(self):
        self.find_by_xpath(VenuesConstants.FEATURES_TAB_VALIDATE_VENUE_ACT_GRP_NAME_CHECKBOX_XPATH).click()

    def is_validate_venue_act_name(self):
        return self.is_checkbox_selected(VenuesConstants.FEATURES_TAB_VALIDATE_VENUE_ACT_GRP_NAME_CHECKBOX_XPATH)

    def click_on_support_trading_phase(self):
        self.find_by_xpath(VenuesConstants.FEATURES_TAB_SUPPORT_TRADING_PHASE_CHECKBOX_XPATH).click()

    def is_support_trading_phase_selected(self):
        return self.is_checkbox_selected(VenuesConstants.FEATURES_TAB_SUPPORT_TRADING_PHASE_CHECKBOX_XPATH)

    def set_market_order_time_in_force(self, value):
        self.set_combobox_value(VenuesConstants.FEATURES_TAB_MARKET_ORDER_TIME_IN_FORCE_XPATH, value)

    def get_market_order_time_in_force(self):
        return self.get_text_by_xpath(VenuesConstants.FEATURES_TAB_MARKET_ORDER_TIME_IN_FORCE_XPATH)

    def click_on_algo_included(self):
        self.find_by_xpath(VenuesConstants.FEATURES_TAB_ALGO_INCLUDED_CHECKBOX_XPATH).click()

    def is_algo_included_selected(self):
        return self.is_checkbox_selected(VenuesConstants.FEATURES_TAB_ALGO_INCLUDED_CHECKBOX_XPATH)

    def set_max_validity_days(self, value):
        self.set_text_by_xpath(VenuesConstants.FEATURES_TAB_MAX_VALIDITY_DAYS_XPATH, value)

    def get_max_validity_days(self):
        return self.get_text_by_xpath(VenuesConstants.FEATURES_TAB_MAX_VALIDITY_DAYS_XPATH)

    def set_venue_qualifier(self, value):
        self.set_combobox_value(VenuesConstants.FEATURES_TAB_VENUE_QUALIFIER_XPATH, value)

    def get_venue_qualifier(self):
        return self.get_text_by_xpath(VenuesConstants.FEATURES_TAB_VENUE_QUALIFIER_XPATH)

    def set_short_time_zone(self, value):
        self.set_text_by_xpath(VenuesConstants.FEATURES_TAB_SHORT_TIME_ZONE_XPATH, value)

    def get_short_time_zone(self):
        return self.get_text_by_xpath(VenuesConstants.FEATURES_TAB_SHORT_TIME_ZONE_XPATH)

    def click_on_validate_venue_client_account_name(self):
        self.find_by_xpath(VenuesConstants.FEATURES_TAB_VALIDATE_VENUE_CLIENT_ACCOUNT_NAME_CHECKBOX_XPATH).click()

    def is_validate_venue_client_account_name_selected(self):
        self.is_checkbox_selected(VenuesConstants.FEATURES_TAB_VALIDATE_VENUE_CLIENT_ACCOUNT_NAME_CHECKBOX_XPATH)

    def set_auto_rfq_timeout(self, value):
        self.set_text_by_xpath(VenuesConstants.FEATURES_TAB_AUTO_RFQ_TIMEOUT_XPATH, value)

    def get_auto_rfq_timeout(self):
        return self.get_text_by_xpath(VenuesConstants.FEATURES_TAB_AUTO_RFQ_TIMEOUT_XPATH)
