from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.venues.venues_constants import VenuesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesTradingPhaseProfileSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(VenuesConstants.TRADING_PHASE_PROFILES_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(VenuesConstants.TRADING_PHASE_PROFILES_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(VenuesConstants.TRADING_PHASE_PROFILES_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(VenuesConstants.TRADING_PHASE_PROFILES_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(VenuesConstants.TRADING_PHASE_PROFILES_TAB_DELETE_BUTTON_XPATH).click()

    def set_trading_phase_profile_desc(self, value):
        self.set_text_by_xpath(VenuesConstants.TRADING_PHASE_PROFILES_TAB_TRADING_PHASE_PROFILE_DESC_XPATH, value)

    def get_trading_phase_profile_desc(self):
        return self.get_text_by_xpath(VenuesConstants.TRADING_PHASE_PROFILES_TAB_TRADING_PHASE_PROFILE_DESC_XPATH)

    def set_trading_phase_profile_desc_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.TRADING_PHASE_PROFILES_TAB_TRADING_PHASE_PROFILE_DESC_FILTER_XPATH,
                               value)

    def is_field_trading_phase_profile_desc_required(self):
        return self.is_field_required(VenuesConstants.TRADING_PHASE_PROFILES_TAB_TRADING_PHASE_PROFILE_DESC_XPATH)

    def is_searched_trading_phase_profile_found(self, value):
        return self.is_element_present(VenuesConstants.TRADING_PHASE_PROFILES_TAB_TRADING_PHASE_PROFILE_DISPLAYED_ENTITY_XPATH.format(value))
    # --------------------Trading phase profile sequences

    def click_on_plus_button_at_trading_phase_profile_sequences(self):
        self.find_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark_at_trading_phase_profile_sequences(self):
        self.find_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close_at_trading_phase_profile_sequences(self):
        self.find_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit_at_trading_phase_profile_sequences(self):
        self.find_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete_at_trading_phase_profile_sequences(self):
        self.find_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_DELETE_BUTTON).click()

    def click_on_submit_allowed(self):
        self.find_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_SUBMIT_ALLOWED_XPATH).click()

    def is_submit_allowed_selected(self):
        return self.is_checkbox_selected(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_SUBMIT_ALLOWED_XPATH)

    def set_submit_allowed_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_SUBMIT_ALLOWED_FILTER_XPATH, value)

    def set_trading_phase(self, value):
        self.set_combobox_value(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_TRADING_PHASE_XPATH, value)

    def get_trading_phase(self):
        return self.get_text_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_TRADING_PHASE_XPATH)

    def set_trading_phase_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_TRADING_PHASE_FILTER_XPATH, value)

    def set_standart_trading_phase(self, value):
        self.set_combobox_value(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_STANDART_TRADING_PHASE_XPATH, value)

    def get_standart_trading_phase(self):
        return self.get_text_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_STANDART_TRADING_PHASE_XPATH)

    def set_standart_trading_phase_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_STANDART_TRADING_PHASE_FILTER_XPATH,
                               value)

    def set_expiry_cycle(self, value):
        self.set_combobox_value(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_EXPIRY_CYCLE_XPATH, value)

    def get_expiry_cycle(self):
        return self.get_text_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_EXPIRY_CYCLE_XPATH)

    def set_expiry_cycle_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_EXPIRY_CYCLE_FILTER_XPATH, value)

    def set_begin_time(self, value):
        self.set_text_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_BEGIN_TIME_XPATH, value)

    def get_begin_time(self):
        return self.get_text_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_BEGIN_TIME_XPATH)

    def set_begin_time_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_BEGIN_TIME_FILTER_XPATH, value)

    def set_end_time(self, value):
        self.set_text_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_END_TIME_XPATH, value)

    def get_end_time(self):
        return self.get_text_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_END_TIME_XPATH)

    def set_end_time_filter(self, value):
        self.set_text_by_xpath(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_END_TIME_FILTER_XPATH, value)

    def is_trading_phase_sequence_field_required(self):
        return self.is_field_required(VenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TAB_TRADING_PHASE_XPATH)

