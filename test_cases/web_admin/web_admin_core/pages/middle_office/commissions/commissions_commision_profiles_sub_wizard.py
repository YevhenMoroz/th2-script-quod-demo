from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.middle_office.commissions.commissions_constants import CommissionsConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class CommissionsCommissionProfilesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        self.find_by_xpath(CommissionsConstants.COMMISSION_PROFILES_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(CommissionsConstants.COMMISSION_PROFILES_CHECKMARK_BUTTON_XPATH).click()

    def click_on_cancel(self):
        self.find_by_xpath(CommissionsConstants.COMMISSION_PROFILES_CANCEL_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(CommissionsConstants.COMMISSION_PROFILES_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(CommissionsConstants.COMMISSION_PROFILES_DELETE_BUTTON_XPATH).click()

    def set_commission_profile_name(self, value):
        self.set_text_by_xpath(CommissionsConstants.COMMISSION_PROFILES_COMMISSION_PROFILE_NAME_XPATH, value)

    def get_commission_profile_name(self):
        return self.get_text_by_xpath(CommissionsConstants.COMMISSION_PROFILES_COMMISSION_PROFILE_NAME_XPATH)

    def set_description(self, value):
        self.set_text_by_xpath(CommissionsConstants.COMMISSION_PROFILES_DESCRIPTION_XPATH, value)

    def get_description(self):
        return self.get_text_by_xpath(CommissionsConstants.COMMISSION_PROFILES_DESCRIPTION_XPATH)

    def set_comm_xunit(self, value):
        self.set_combobox_value(CommissionsConstants.COMMISSION_PROFILES_COMM_XUNIT_XPATH, value)

    def get_comm_xunit(self):
        return self.get_text_by_xpath(CommissionsConstants.COMMISSION_PROFILES_COMM_XUNIT_XPATH)

    def set_venue_commission_profile_id(self, value):
        self.set_text_by_xpath(CommissionsConstants.COMMISSION_PROFILES_VENUE_COMMISSION_PROFILE_ID_XPATH, value)

    def get_venue_commission_profile_id(self):
        return self.get_text_by_xpath(CommissionsConstants.COMMISSION_PROFILES_VENUE_COMMISSION_PROFILE_ID_XPATH)

    def set_comm_type(self, value):
        self.set_combobox_value(CommissionsConstants.COMMISSION_PROFILES_COMM_TYPE_XPATH, value)

    def get_comm_type(self):
        return self.get_text_by_xpath(CommissionsConstants.COMMISSION_PROFILES_COMM_TYPE_XPATH)

    def set_comm_algorithm(self, value):
        self.set_combobox_value(CommissionsConstants.COMMISSION_PROFILES_COMM_ALGORITHM_XPATH, value)

    def get_comm_algorithm(self):
        return self.get_text_by_xpath(CommissionsConstants.COMMISSION_PROFILES_COMM_ALGORITHM_XPATH)

    def set_max_commission(self, value):
        self.set_text_by_xpath(CommissionsConstants.COMMISSION_PROFILES_MAX_COMMISSION_XPATH, value)

    def get_max_commission(self):
        return self.get_text_by_xpath(CommissionsConstants.COMMISSION_PROFILES_MAX_COMMISSION_XPATH)

    def set_currency(self, value):
        self.set_combobox_value(CommissionsConstants.COMMISSION_PROFILES_CURRENCY_XPATH, value)

    def get_currency(self):
        return self.get_text_by_xpath(CommissionsConstants.COMMISSION_PROFILES_CURRENCY_XPATH)

    def set_rounding_direction(self, value):
        self.set_combobox_value(CommissionsConstants.COMMISSION_PROFILES_ROUNDING_DIRECTION_XPATH, value)

    def get_rounding_direction(self):
        return self.get_text_by_xpath(CommissionsConstants.COMMISSION_PROFILES_ROUNDING_DIRECTION_XPATH)

    def set_rounding_precision(self, value):
        self.set_text_by_xpath(CommissionsConstants.COMMISSION_PROFILES_ROUNDING_PRECISION_XPATH, value)

    def get_rounding_precision(self):
        return self.get_text_by_xpath(CommissionsConstants.COMMISSION_PROFILES_ROUNDING_PRECISION_XPATH)

    def set_rounding_modulus(self, value):
        self.set_text_by_xpath(CommissionsConstants.COMMISSION_PROFILES_ROUNDING_PRECISION_XPATH, value)

    def get_rounding_modulus(self):
        return self.get_text_by_xpath(CommissionsConstants.COMMISSION_PROFILES_ROUNDING_PRECISION_XPATH)

    def set_commission_profile_name_filter(self, value):
        self.set_text_by_xpath(CommissionsConstants.COMMISSION_PROFILES_COMMISSION_PROFILE_NAME_FILTER_XPATH, value)
