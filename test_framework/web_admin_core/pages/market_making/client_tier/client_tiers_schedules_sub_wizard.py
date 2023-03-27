from selenium.webdriver.common.action_chains import ActionChains
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_constants import \
    ClientTierConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientTiersSchedulesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button_at_schedule_name(self):
        """
        ActionChains helps to avoid falling test when adding several quantities at once.
        (The usual "click" method fails because after adding the first entry, the cursor remains on the "edit" button
        and the pop-up of edit btn covers half of the "+" button)
        """
        element = self.find_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_NAME_TAB_PLUS_BUTTON)
        action = ActionChains(self.web_driver_container.get_driver())
        action.move_to_element(element)
        action.click()
        action.perform()

    def click_on_checkmark_button_at_schedule_name(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_NAME_TAB_CHECKMARK_XPATH).click()

    def click_on_close_button_at_schedule_name(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_NAME_TAB_CANCEL_XPATH).click()

    def click_on_edit_button_at_schedule_name(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_NAME_TAB_EDIT_XPATH).click()

    def click_on_delete_button_at_schedule_name(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_NAME_TAB_DELETE_XPATH).click()

    def set_schedule_name(self, name):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_NAME_TAB_NAME_XPATH, name)

    def set_schedule_name_filter(self, name):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_SCHEDULES_NAME_TAB_NAME_FILTER_XPATH, name)

    def is_schedule_name_entity_found_by_name(self, name):
        return self.is_element_present(ClientTierConstants.CLIENT_TIER_SCHEDULES_NAME_TAB_SEARCHED_ENTITY_XPATH.format(name))

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
        self.select_value_from_dropdown_list(ClientTierConstants.CLIENT_TIER_SCHEDULES_TAB_DAY_XPATH, value)

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
