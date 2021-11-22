from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.reference_data.subvenues.subvenues_constants import SubVenuesConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class SubVenuesDetailsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_trading_status(self, value):
        self.set_combobox_value(SubVenuesConstants.DETAILS_TAB_TRADING_STATUS_XPATH, value)

    def get_trading_status(self):
        return self.get_text_by_xpath(SubVenuesConstants.DETAILS_TAB_TRADING_STATUS_XPATH)

    def set_price_limit_profile(self, value):
        self.set_combobox_value(SubVenuesConstants.DETAILS_TAB_PRICE_LIMIT_PROFILE_XPATH, value)

    def get_price_limit_profile(self):
        self.get_text_by_xpath(SubVenuesConstants.DETAILS_TAB_PRICE_LIMIT_PROFILE_XPATH)

    def set_trading_phase_profile(self, value):
        self.set_combobox_value(SubVenuesConstants.DETAILS_TAB_TRADING_PHASE_PROFILE_XPATH, value)

    def get_trading_phase_profile(self):
        return self.get_text_by_xpath(SubVenuesConstants.DETAILS_TAB_TRADING_PHASE_PROFILE_XPATH)

    def set_trading_phase(self, value):
        self.set_combobox_value(SubVenuesConstants.DETAILS_TAB_TRADING_PHASE_XPATH, value)

    def get_trading_phase(self):
        return self.get_text_by_xpath(SubVenuesConstants.DETAILS_TAB_TRADING_PHASE_XPATH)

    def set_tick_size_profile(self, value):
        self.set_combobox_value(SubVenuesConstants.DETAILS_TAB_TICK_SIZE_PROFILE_XPATH, value)

    def get_tick_size_profile(self):
        self.get_text_by_xpath(SubVenuesConstants.DETAILS_TAB_TICK_SIZE_PROFILE_XPATH)

    def click_on_manage_price_limit_profile(self):
        self.find_by_xpath(SubVenuesConstants.DETAILS_TAB_MANAGE_PRICE_LIMIT_PROFILE_XPATH).click()

    def click_on_manage_trading_phase_profile(self):
        self.find_by_xpath(SubVenuesConstants.DETAILS_TAB_MANAGE_TRADING_PHASE_PROFILE_XPATH).click()

    def click_on_manage_tick_size_profile(self):
        self.find_by_xpath(SubVenuesConstants.DETAILS_TAB_MANAGE_TICK_SIZE_PROFILE_XPATH).click()
