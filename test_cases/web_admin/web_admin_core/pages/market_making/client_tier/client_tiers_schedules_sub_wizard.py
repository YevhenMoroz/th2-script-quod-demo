from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.market_making.client_tier.client_tier_constants import \
    ClientTierConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientTiersSchedulesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_enable_schedule_checkbox(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_TAB_ENABLE_SCHEDULE_CHECKBOX_XPATH).click()

    # region schedules

    def click_on_plus_button_at_schedules(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark_button_at_schedules(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close_button_at_schedules(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit_button_at_schedules(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete_button_at_schedules(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_TAB_DELETE_BUTTON_XPATH).click()

    def set_day(self, value):
        self.set_combobox_value(ClientTierConstants.CLIENT_TIER_SCHEDULES_TAB_DAY_XPATH, value)

    def get_day(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_TAB_DAY_XPATH)

    def set_from_time(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_TAB_FROM_TIME_XPATH, value)

    def get_from_time(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_TAB_FROM_TIME_XPATH)

    def set_to_time(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_TAB_TO_TIME_XPATH, value)

    def get_to_time(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_TAB_TO_TIME_XPATH)

    def set_day_filter(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_TAB_DAY_FILTER_XPATH, value)

    def set_from_time_filter(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_TAB_FROM_TIME_FILTER_XPATH, value)

    def set_to_time_filter(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_TAB_TO_TIME_FILTER_XPATH, value)

    # endregion

    # region schedule Exceptions

    def click_on_plus_button_at_schedule_exceptions(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark_at_schedule_exceptions(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close_button_at_schedule_exceptions(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_delete_button_at_schedule_exceptions(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_TAB_DELETE_BUTTON_XPATH).click()

    def set_exception_date_at_schedule_exceptions(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_EXCEPTION_DAY_XPATH, value)

    def get_exception_date_at_schedule_exceptions(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_EXCEPTION_DAY_XPATH)

    def set_from_time_at_schedule_exceptions(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_FROM_TIME_XPATH, value)

    def get_from_time_at_schedule_exceptions(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_FROM_TIME_XPATH)

    def set_exception_date_filter_at_schedule_exceptions(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_EXCEPTION_DAY_FILTER_XPATH,
                               value)

    def set_from_time_filter_at_schedule_exceptions(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_FROM_TIME_FILTER_XPATH, value)

    def set_to_time_filter_at_schedule_exceptions(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_TO_TIME_FILTER_XPATH, value)

    # endregion
