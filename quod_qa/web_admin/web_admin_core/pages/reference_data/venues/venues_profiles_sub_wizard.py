from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.venues.venues_constants import VenuesConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesProfilesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_price_limit_profile(self, value):
        self.set_combobox_value(VenuesConstants.PROFILES_TAB_PRICE_LIMIT_PROFILE_XPATH, value)

    def get_price_limit_profile(self):
        return self.get_text_by_xpath(VenuesConstants.PROFILES_TAB_PRICE_LIMIT_PROFILE_XPATH)

    def set_tick_size_profile(self, value):
        self.set_combobox_value(VenuesConstants.PROFILES_TAB_TICK_SIZE_PROFILE_XPATH, value)

    def get_tick_size_profile(self):
        return self.get_text_by_xpath(VenuesConstants.PROFILES_TAB_TICK_SIZE_PROFILE_XPATH)

    def set_holiday(self, value):
        self.set_combobox_value(VenuesConstants.PROFILES_TAB_HOLIDAY_XPATH, value)

    def get_holiday(self):
        return self.get_text_by_xpath(VenuesConstants.PROFILES_TAB_HOLIDAY_XPATH)

    def set_anti_crossing_period(self, value):
        self.set_text_by_xpath(VenuesConstants.PROFILES_TAB_ANTI_CROSSING_PERIOD_XPATH, value)

    def get_anti_crossing_period(self):
        return self.get_text_by_xpath(VenuesConstants.PROFILES_TAB_ANTI_CROSSING_PERIOD_XPATH)

    def set_trading_phase_profile(self, value):
        self.set_combobox_value(VenuesConstants.PROFILES_TAB_TRADING_PHASE_PROFILE_XPATH, value)

    def get_trading_phase_profile(self):
        return self.get_text_by_xpath(VenuesConstants.PROFILES_TAB_TRADING_PHASE_PROFILE_XPATH)

    def set_routing_param_group(self, value):
        self.set_combobox_value(VenuesConstants.PROFILES_TAB_ROUTING_PARAM_GROUP_XPATH, value)

    def get_routing_param_group(self):
        return self.get_text_by_xpath(VenuesConstants.PROFILES_TAB_ROUTING_PARAM_GROUP_XPATH)

    def set_weekend_day(self, value):
        self.set_checkbox_list(VenuesConstants.PROFILES_TAB_WEEKEND_DAY_XPATH, value)

    def get_weekend_day(self):
        pass

    def click_on_price_limit_profile_mange_button(self):
        self.find_by_xpath(VenuesConstants.PROFILES_TAB_PRICE_LIMIT_PROFILE_MANAGE_BUTTON_XPATH).click()

    def click_on_tick_size_profile_manage_button(self):
        self.find_by_xpath(VenuesConstants.PROFILES_TAB_TICK_SIZE_PROFILE_MANAGE_BUTTON_XPATH).click()

    def click_on_holiday_manage_button(self):
        self.find_by_xpath(VenuesConstants.PROFILES_TAB_HOLIDAY_MANAGE_BUTTON_XPATH).click()

    def click_on_trading_phase_profile_mange_button(self):
        self.find_by_xpath(VenuesConstants.PROFILES_TAB_TRADING_PHASE_PROFILE_MANAGE_BUTTON_XPATH).click()

    def click_on_routing_param_group(self):
        self.find_by_xpath(VenuesConstants.PROFILES_TAB_ROUTING_PARAM_GROUP_MANAGE_BUTTON_XPATH).click()
