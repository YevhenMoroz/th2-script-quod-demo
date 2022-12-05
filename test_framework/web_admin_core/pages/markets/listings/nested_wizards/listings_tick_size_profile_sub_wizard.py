from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.listings.listings_constants import ListingsConstants

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingsTickSizeProfileSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(ListingsConstants.TICK_SIZE_PROFILES_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(ListingsConstants.TICK_SIZE_PROFILES_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(ListingsConstants.TICK_SIZE_PROFILES_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ListingsConstants.TICK_SIZE_PROFILES_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(ListingsConstants.TICK_SIZE_PROFILES_TAB_DELETE_BUTTON_XPATH).click()

    def set_external_id(self, value):
        self.set_text_by_xpath(ListingsConstants.TICK_SIZE_PROFILES_TAB_EXTERNAL_ID_XPATH, value)

    def get_external_id(self):
        return self.get_text_by_xpath(ListingsConstants.TICK_SIZE_PROFILES_TAB_EXTERNAL_ID_XPATH)

    def set_external_id_filter(self, value):
        self.set_text_by_xpath(ListingsConstants.TICK_SIZE_PROFILES_TAB_EXTERNAL_ID_FILTER_XPATH, value)

    def set_tick_size_xaxis_type(self, value):
        self.set_combobox_value(ListingsConstants.TICK_SIZE_PROFILES_TAB_TICK_SIZE_XAXIS_TYPE_XPATH, value)

    def get_tick_size_xaxis_type(self):
        return self.get_text_by_xpath(ListingsConstants.TICK_SIZE_PROFILES_TAB_TICK_SIZE_XAXIS_TYPE_XPATH)

    def set_tick_xaxis_type_filter(self, value):
        self.set_text_by_xpath(ListingsConstants.TICK_SIZE_PROFILES_TAB_TICK_SIZE_XAXIS_TYPE_FILTER_XPATH, value)

    def set_tick_size_refprice_type(self, value):
        self.set_combobox_value(ListingsConstants.TICK_SIZE_PROFILES_TAB_TICK_SIZE_REFPRICE_TYPE_XPATH, value)

    def get_tick_size_refprice_type(self):
        return self.get_text_by_xpath(ListingsConstants.TICK_SIZE_PROFILES_TAB_TICK_SIZE_REFPRICE_TYPE_XPATH)

    def set_tick_size_refprice_type_filter(self, value):
        self.set_text_by_xpath(ListingsConstants.TICK_SIZE_PROFILES_TAB_TICK_SIZE_REFPRICE_TYPE_FILTER_XPATH, value)

    def click_on_plus_button_at_tick_size_points(self):
        self.find_by_xpath(ListingsConstants.TICK_SIZE_POINTS_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark_at_tick_size_points(self):
        self.find_by_xpath(ListingsConstants.TICK_SIZE_POINTS_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close_at_tick_size_points(self):
        self.find_by_xpath(ListingsConstants.TICK_SIZE_POINTS_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit_at_tick_size_points(self):
        self.find_by_xpath(ListingsConstants.TICK_SIZE_POINTS_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete_at_tick_size_points(self):
        self.find_by_xpath(ListingsConstants.TICK_SIZE_POINTS_TAB_DELETE_BUTTON_XPATH).click()

    def set_tick(self, value):
        self.set_text_by_xpath(ListingsConstants.TICK_SIZE_POINTS_TAB_TICK_XPATH, value)

    def get_tick(self):
        return self.get_text_by_xpath(ListingsConstants.TICK_SIZE_POINTS_TAB_TICK_XPATH)

    def set_tick_filter(self, value):
        self.set_text_by_xpath(ListingsConstants.TICK_SIZE_POINTS_TAB_TICK_FILTER_XPATH, value)

    def set_upper_limit(self, value):
        self.set_text_by_xpath(ListingsConstants.TICK_SIZE_POINTS_TAB_UPPER_LIMIT_XPATH, value)

    def get_upper_limit(self):
        return self.get_text_by_xpath(ListingsConstants.TICK_SIZE_POINTS_TAB_UPPER_LIMIT_XPATH)

    def set_upper_limit_filter(self, value):
        self.set_text_by_xpath(ListingsConstants.TICK_SIZE_POINTS_TAB_UPPER_LIMIT_FILTER_XPATH, value)
