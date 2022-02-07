import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_trading.web_trading_core.pages.main_page.menu.profile.profile_constants import ProfileConstants


class ProfilePreferenceSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_show_order_notifications_radio_button(self):
        self.find_by_xpath(ProfileConstants.ORDER_NOTIFICATIONS_SHOW_RADIO_BUTTON_XPATH).click()

    def click_on_hide_order_notifications_radio_button(self):
        self.find_by_xpath(ProfileConstants.ORDER_NOTIFICATIONS_HIDE_RADIO_BUTTON_XPATH).click()

    def click_on_show_execution_notifications_radio_button(self):
        self.find_by_xpath(ProfileConstants.EXECUTION_NOTIFICATIONS_SHOW_RADIO_BATTON_XPATH).click()

    def click_on_hide_execution_notifications_radio_button(self):
        self.find_by_xpath(ProfileConstants.EXECUTION_NOTIFICATIONS_HIDE_RADIO_BATTON_XPATH).click()

    def click_on_show_other_notifications_radio_button(self):
        self.find_by_xpath(ProfileConstants.OTHER_NOTIFICATIONS_SHOW_RADIO_BUTTON_XPATH).click()

    def click_on_hide_other_notifications_radio_button(self):
        self.find_by_xpath(ProfileConstants.OTHER_NOTIFICATIONS_HIDE_RADIO_BUTTON_XPATH).click()

    def set_default_client_from_dropdown_list(self, default_client_name):
        self.find_by_xpath(ProfileConstants.DEFAULT_CLIENT_SELECT_MENU_XPATH).click()
        time.sleep(2)
        self.select_value_from_dropdown_list(ProfileConstants.LIST_OF_DEFAULT_CLIENTS_XPATH.format(default_client_name))
