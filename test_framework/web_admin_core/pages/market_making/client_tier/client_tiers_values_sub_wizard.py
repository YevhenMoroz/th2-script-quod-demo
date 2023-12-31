import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_constants import \
    ClientTierConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientTiersValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_NAME_XPATH)

    def set_core_spot_price_strategy(self, value):
        self.select_value_from_dropdown_list(ClientTierConstants.CLIENT_TIER_VALUES_TAB_CORE_SPOT_PRICE_STRATEGY_XPATH, value)

    def clear_field_core_spot_price_strategy(self):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_CORE_SPOT_PRICE_STRATEGY_XPATH, "")

    def get_core_spot_price_strategy(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_CORE_SPOT_PRICE_STRATEGY_XPATH)

    def get_all_core_spot_price_strategy_from_drop_menu(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_CORE_SPOT_PRICE_STRATEGY_XPATH).click()
        time.sleep(2)
        return self.get_all_items_from_drop_down(ClientTierConstants.CLIENT_TIER_VALUES_TAB_CORE_SPOT_PRICE_STRATEGY_DROP_DOWN_MENU_XPATH)

    def set_tod_time_zone(self, value):
        self.set_combobox_value(ClientTierConstants.CLIENT_TIER_VALUES_TAB_TOD_TIME_ZONE, value)

    def get_tod_time_zone(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_TOD_TIME_ZONE)

    def set_tod_start_time(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_TOD_START_TIME, value)

    def get_tod_start_time(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_TOD_START_TIME)

    def set_tod_end_time(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_TOD_END_TIME, value)

    def get_tod_end_time(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_TOD_END_TIME)

    def select_schedule_checkbox(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_SCHEDULES_CHECKBOX).click()

    def is_schedule_checkbox_selected(self):
        return self.is_checkbox_selected(ClientTierConstants.CLIENT_TIER_VALUES_TAB_SCHEDULES_CHECKBOX)

    def set_schedule(self, value):
        self.set_combobox_value(ClientTierConstants.CLIENT_TIER_VALUES_TAB_SCHEDULES, value)

    def get_schedule(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_SCHEDULES)

    def get_all_schedules_from_drop_menu(self):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_SCHEDULES, "")
        time.sleep(1)
        return self.get_all_items_from_drop_down(ClientTierConstants.DROP_DOWN_MENU_XPATH)

    def click_on_manage_button_for_schedules(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_VALUES_TAB_SCHEDULES_MANAGE_BUTTON).click()
