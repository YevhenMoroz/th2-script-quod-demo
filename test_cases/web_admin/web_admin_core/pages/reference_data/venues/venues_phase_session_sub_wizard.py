from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_constants import VenuesConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesPhaseSessionSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(VenuesConstants.PHASE_SESSION_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(VenuesConstants.PHASE_SESSION_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(VenuesConstants.PHASE_SESSION_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(VenuesConstants.PHASE_SESSION_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(VenuesConstants.PHASE_SESSION_TAB_DELETE_BUTTON_XPATH).click()

    def set_trading_phase(self, value):
        self.set_combobox_value(VenuesConstants.PHASE_SESSION_TAB_TRADING_PHASE_XPATH, value)

    def set_trading_phase_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.PHASE_SESSION_TAB_TRADING_PHASE_FILTER_XPATH, value)

    def get_trading_phase(self):
        return self.get_text_by_xpath(VenuesConstants.PHASE_SESSION_TAB_TRADING_PHASE_XPATH)

    def set_trading_session(self, value):
        self.set_text_by_xpath(VenuesConstants.PHASE_SESSION_TAB_TRADING_SESSION_XPATH, value)

    def set_trading_session_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.PHASE_SESSION_TAB_TRADING_SESSION_FILTER_XPATH, value)

    def get_trading_session(self):
        return self.get_text_by_xpath(VenuesConstants.PHASE_SESSION_TAB_TRADING_SESSION_XPATH)

    def click_on_support_min_quantity(self):
        self.find_by_xpath(VenuesConstants.PHASE_SESSION_TAB_SUPPORT_MIN_QUANTITY_XPATH).click()

    def set_support_min_quantity_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.PHASE_SESSION_TAB_SUPPORT_MIN_QUANTITY_FILTER_XPATH, value)

    def is_support_min_quantity_selected(self):
        self.is_checkbox_selected(VenuesConstants.PHASE_SESSION_TAB_SUPPORT_MIN_QUANTITY_XPATH)

    def set_peg_price_type(self, value):
        self.set_checkbox_list(VenuesConstants.PHASE_SESSION_TAB_PEG_PRICE_TYPE_XPATH, value)

    def set_peg_price_type_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.PHASE_SESSION_TAB_PEG_PRICE_TYPE_FILTER_XPATH, value)

    # ------------TIF-------------------------------------------------------------------------------------------

    def click_on_plus_button_at_type_tif(self):
        self.find_by_xpath(VenuesConstants.TYPE_TIF_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark_at_type_tif(self):
        self.find_by_xpath(VenuesConstants.TYPE_TIF_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close_at_type_tif(self):
        self.find_by_xpath(VenuesConstants.TYPE_TIF_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit_at_type_tif(self):
        self.find_by_xpath(VenuesConstants.TYPE_TIF_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete_at_type_tif(self):
        self.find_by_xpath(VenuesConstants.TYPE_TIF_TAB_DELETE_BUTTON_XPATH).click()

    def set_time_in_force(self, value):
        self.set_combobox_value(VenuesConstants.TYPE_TIF_TAB_TIME_IN_FORCE_XPATH, value)

    def set_time_in_force_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.TYPE_TIF_TAB_TIME_IN_FORCE_FILTER_XPATH, value)

    def get_time_in_force(self):
        return self.get_text_by_xpath(VenuesConstants.TYPE_TIF_TAB_TIME_IN_FORCE_XPATH)

    def set_odr_type(self, value):
        self.set_combobox_value(VenuesConstants.TYPE_TIF_TAB_ORD_TYPE_XPATH, value)

    def set_ord_type_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.TYPE_TIF_TAB_ORD_TYPE_FILTER_XPATH, value)

    def get_ord_type(self):
        return self.get_text_by_xpath(VenuesConstants.TYPE_TIF_TAB_ORD_TYPE_XPATH)

    def click_on_support_display_quantity(self):
        self.find_by_xpath(VenuesConstants.TYPE_TIF_TAB_SUPPORT_DISPLAY_QUANTITY_CHECKBOX_XPATH).click()

    def set_support_display_quantity(self, value):
        self.set_text_by_xpath(VenuesConstants.TYPE_TIF_TAB_SUPPORT_DISPLAY_QUANTITY_CHECKBOX_FILTER_XPATH, value)

    def is_support_display_quantity_selected(self):
        return self.is_checkbox_selected(VenuesConstants.TYPE_TIF_TAB_SUPPORT_DISPLAY_QUANTITY_CHECKBOX_XPATH)
