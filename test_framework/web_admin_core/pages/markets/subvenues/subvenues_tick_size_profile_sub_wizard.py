from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.subvenues.subvenues_constants import SubVenuesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class SubVenuesTickSizeProfilesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_at_profiles(self):
        self.find_by_xpath(SubVenuesConstants.TICK_SIZE_PROFILE_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark_at_profiles(self):
        self.find_by_xpath(SubVenuesConstants.TICK_SIZE_PROFILE_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close_at_profiles(self):
        self.find_by_xpath(SubVenuesConstants.TICK_SIZE_PROFILE_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit_at_profiles(self):
        self.find_by_xpath(SubVenuesConstants.TICK_SIZE_PROFILE_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete_at_profiles(self):
        self.find_by_xpath(SubVenuesConstants.TICK_SIZE_PROFILE_TAB_DELETE_BUTTON_XPATH).click()

    def set_external_id(self, value):
        self.set_text_by_xpath(SubVenuesConstants.TICK_SIZE_PROFILE_TAB_EXTERNAL_ID_XPATH, value)

    def set_external_id_filter(self, value):
        self.set_text_by_xpath(SubVenuesConstants.TICK_SIZE_PROFILE_TAB_EXTERNAL_ID_FILTER_XPATH, value)

    def get_external_id(self):
        return self.get_text_by_xpath(SubVenuesConstants.TICK_SIZE_PROFILE_TAB_EXTERNAL_ID_XPATH)

    def set_tick_xaxis_type(self, value):
        self.set_combobox_value(SubVenuesConstants.TICK_SIZE_PROFILE_TAB_TICK_SIZE_XAXIS_TYPE_XPATH, value)

    def set_tick_xaxis_type_filter(self, value):
        self.set_text_by_xpath(SubVenuesConstants.TICK_SIZE_PROFILE_TAB_TICK_SIZE_XAXIS_TYPE_FILTER_XPATH, value)

    def get_tick_xaxis_type(self):
        return self.get_text_by_xpath(SubVenuesConstants.TICK_SIZE_PROFILE_TAB_TICK_SIZE_XAXIS_TYPE_XPATH)

    def set_tick_size_refprice_type(self, value):
        self.set_combobox_value(SubVenuesConstants.TICK_SIZE_PROFILE_TAB_TICK_SIZE_REFPRICE_TYPE_XPATH, value)

    def set_tick_size_refprice_type_filter(self, value):
        self.set_text_by_xpath(SubVenuesConstants.TICK_SIZE_PROFILE_TAB_TICK_SIZE_REFPRICE_TYPE_FILTER_XPATH, value)

    def get_tick_size_refprice_type(self):
        return self.get_text_by_xpath(SubVenuesConstants.TICK_SIZE_PROFILE_TAB_TICK_SIZE_REFPRICE_TYPE_XPATH)

    # -----------------------
    def click_on_plus_at_points(self):
        self.find_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark_at_points(self):
        self.find_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close_at_points(self):
        self.find_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_CLOSE_BUTTON_XPATH).click()

    def click_on_edit_at_points(self):
        self.find_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_EDIT_BUTTON_XPATH).click()

    def click_on_delete_at_points(self):
        self.find_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_DELETE_BUTTON_XPATH).click()

    def set_tick(self, value):
        self.set_text_by_xpath(SubVenuesConstants.TICK_SIZE_POINTS_TICK_XPATH, value)

    def set_tick_filter(self, value):
        self.set_text_by_xpath(SubVenuesConstants.TICK_SIZE_POINTS_TICK_FILTER_XPATH, value)

    def get_tick(self):
        return self.get_text_by_xpath(SubVenuesConstants.TICK_SIZE_POINTS_TICK_XPATH)

    def set_upper_limit(self, value):
        self.set_text_by_xpath(SubVenuesConstants.PRICE_LIMIT_POINTS_TAB_UPPER_LIMIT_XPATH, value)

    def set_upper_limit_filter(self, value):
        self.set_text_by_xpath(SubVenuesConstants.PRICE_LIMIT_POINTS_TAB_UPPER_LIMIT_FILTER_XPATH, value)

    def get_upper_limit(self):
        return self.get_text_by_xpath(SubVenuesConstants.PRICE_LIMIT_POINTS_TAB_UPPER_LIMIT_XPATH)
