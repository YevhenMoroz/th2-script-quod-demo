from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.subvenues.subvenues_constants import SubVenuesConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class SubVenuesTradingPhaseProfileSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_at_profiles(self):
        self.find_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILES_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark_at_profiles(self):
        self.find_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILES_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close_at_profiles(self):
        self.find_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILES_CLOSE_BUTTON_XPATH).click()

    def click_on_edit_at_profiles(self):
        self.find_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILES_EDIT_BUTTON_XPATH).click()

    def click_on_delete_at_profiles(self):
        self.find_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILES_DELETE_BUTTON_XPATH).click()

    def set_trading_phase_profile_desc(self, value):
        self.set_text_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILES_TRADING_PHASE_PROFILE_DESC_XPATH, value)

    def set_trading_phase_profile_desc_filter(self, value):
        self.set_text_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILES_TRADING_PHASE_PROFILE_DESC_FILTER_XPATH, value)

    def get_trading_phase_profile_desc(self):
        return self.get_text_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILES_TRADING_PHASE_PROFILE_DESC_XPATH)

    # -----------------------
    def click_on_plus_at_sequences(self):
        self.find_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark_at_sequences(self):
        self.find_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close_at_sequences(self):
        self.find_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_CLOSE_BUTTON_XPATH).click()

    def click_on_edit_at_sequences(self):
        self.find_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_EDIT_BUTTON_XPATH).click()

    def click_on_delete_at_sequences(self):
        self.find_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_DELETE_BUTTON_XPATH).click()

    def click_on_submit_allowed(self):
        self.find_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_SUBMIT_ALLOWED_CHECKBOX_XPATH).click()

    def set_trading_phase(self, value):
        self.set_combobox_value(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TRADING_PHASE_XPATH, value)

    def set_trading_phase_filter(self, value):
        self.set_text_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TRADING_PHASE_FILTER_XPATH, value)

    def get_trading_phase(self):
        return self.get_text_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_TRADING_PHASE_XPATH)

    def set_standart_trading_phase(self, value):
        self.set_combobox_value(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_STANDART_TRADING_PHASE_XPATH, value)

    def set_standart_trading_phase_filter(self, value):
        self.set_text_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_STANDART_TRADING_PHASE_FILTER_XPATH,
                               value)

    def get_standart_trading_phase(self):
        return self.get_text_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_STANDART_TRADING_PHASE_XPATH)

    def set_expiry_cycle(self, value):
        self.set_combobox_value(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_EXPIRY_CYCLE_XPATH, value)

    def set_expiry_cycle_filter(self, value):
        self.set_combobox_value(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_EXPIRY_CYCLE_FILTER_XPATH, value)

    def get_expiry_cycle(self):
        return self.get_text_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_EXPIRY_CYCLE_XPATH)

    def set_begin_time(self, value):
        self.set_text_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_BEGIN_TIME_XPATH, value)

    def set_begin_time_filter(self, value):
        self.set_text_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_BEGIN_TIME_FILTER_XPATH, value)

    def get_begin_time(self):
        return self.get_text_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_BEGIN_TIME_XPATH)

    def set_end_time(self, value):
        self.set_text_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_END_TIME_XPATH, value)

    def set_end_time_filter(self, value):
        self.set_text_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_END_TIME_FILTER_XPATH, value)

    def get_end_time(self):
        return self.get_text_by_xpath(SubVenuesConstants.TRADING_PHASE_PROFILE_SEQUENCES_END_TIME_XPATH)
