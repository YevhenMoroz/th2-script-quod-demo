from selenium.webdriver import ActionChains

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_constants import FeesConstants

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class FeesExecFeeProfileSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        """
        ActionChains helps to avoid falling test when adding several quantities at once.
        (The usual "click" method fails because after adding the first entry, the cursor remains on the "edit" button
        and the pop-up of edit btn covers half of the "+" button)
        """
        element = self.find_by_xpath(FeesConstants.EXEC_FEE_PROFILE_PLUS_BUTTON_XPATH)
        action = ActionChains(self.web_driver_container.get_driver())
        action.move_to_element(element).click().perform()

    def click_on_checkmark(self):
        self.find_by_xpath(FeesConstants.EXEC_FEE_PROFILE_CHECKMARK_BUTTON_XPATH).click()

    def click_on_cancel(self):
        self.find_by_xpath(FeesConstants.EXEC_FEE_PROFILE_CANCEL_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(FeesConstants.EXEC_FEE_PROFILE_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(FeesConstants.EXEC_FEE_PROFILE_DELETE_BUTTON_XPATH).click()

    def set_commission_profile_name_filter(self, value):
        self.set_text_by_xpath(FeesConstants.EXEC_FEE_PROFILE_COMMISSION_PROFILE_FILTER_XPATH, value)

    def set_commission_profile_name(self, value):
        self.set_text_by_xpath(FeesConstants.EXEC_FEE_PROFILE_COMMISSION_PROFILE_NAME_XPATH, value)

    def get_commission_profile_name(self):
        return self.get_text_by_xpath(FeesConstants.EXEC_FEE_PROFILE_COMMISSION_PROFILE_NAME_XPATH)

    def set_description(self, value):
        self.set_text_by_xpath(FeesConstants.EXEC_FEE_PROFILE_DESCRIPTION_XPATH, value)

    def get_description(self):
        return self.get_text_by_xpath(FeesConstants.EXEC_FEE_PROFILE_DESCRIPTION_XPATH)

    def set_comm_xunit(self, value):
        self.select_value_from_dropdown_list(FeesConstants.EXEC_FEE_PROFILE_COMM_XUNIT_XPATH, value)

    def get_comm_xunit(self):
        return self.get_text_by_xpath(FeesConstants.EXEC_FEE_PROFILE_COMM_XUNIT_XPATH)

    def is_comm_xunit_enabled(self):
        return self.is_field_enabled(FeesConstants.EXEC_FEE_PROFILE_COMM_XUNIT_XPATH)

    def set_venue_commission_profile_id(self, value):
        self.set_text_by_xpath(FeesConstants.EXEC_FEE_PROFILE_VENUE_COMMISSION_PROFILE_ID_XPATH, value)

    def get_venue_commission_profile_id(self):
        return self.get_text_by_xpath(FeesConstants.EXEC_FEE_PROFILE_VENUE_COMMISSION_PROFILE_ID_XPATH)

    def set_comm_type(self, value):
        self.select_value_from_dropdown_list(FeesConstants.EXEC_FEE_PROFILE_COMM_TYPE_XPATH, value)

    def get_comm_type(self):
        return self.get_text_by_xpath(FeesConstants.EXEC_FEE_PROFILE_COMM_TYPE_XPATH)

    def set_comm_algorithm(self, value):
        self.select_value_from_dropdown_list(FeesConstants.EXEC_FEE_PROFILE_COMM_ALGORITHM_XPATH, value)

    def get_comm_algorithm(self):
        return self.get_text_by_xpath(FeesConstants.EXEC_FEE_PROFILE_COMM_ALGORITHM_XPATH)

    def set_max_commission(self, value):
        self.set_text_by_xpath(FeesConstants.EXEC_FEE_PROFILE_MAX_COMMISSION_XPATH, value)

    def get_max_commission(self):
        return self.get_text_by_xpath(FeesConstants.EXEC_FEE_PROFILE_MAX_COMMISSION_XPATH)

    def set_currency(self, value):
        self.set_combobox_value(FeesConstants.EXEC_FEE_PROFILE_CURRENCY_XPATH, value)

    def get_currency(self):
        return self.get_text_by_xpath(FeesConstants.EXEC_FEE_PROFILE_CURRENCY_XPATH)

    def set_rounding_direction(self, value):
        self.set_combobox_value(FeesConstants.EXEC_FEE_PROFILE_ROUNDING_DIRECTION_XPATH, value)

    def get_rounding_direction(self):
        return self.get_text_by_xpath(FeesConstants.EXEC_FEE_PROFILE_ROUNDING_DIRECTION_XPATH)

    def set_rounding_precision(self, value):
        self.set_text_by_xpath(FeesConstants.EXEC_FEE_PROFILE_ROUNDING_PRECISION_XPATH, value)

    def get_rounding_precision(self):
        return self.get_text_by_xpath(FeesConstants.EXEC_FEE_PROFILE_ROUNDING_PRECISION_XPATH)

    def set_rounding_modulus(self, value):
        self.set_text_by_xpath(FeesConstants.EXEC_FEE_PROFILE_ROUNDING_PRECISION_XPATH, value)

    def get_rounding_modulus(self):
        return self.get_text_by_xpath(FeesConstants.EXEC_FEE_PROFILE_ROUNDING_PRECISION_XPATH)

    def is_searched_commission_profile_found(self, value):
        return self.is_element_present(FeesConstants.EXEC_FEE_PROFILE_DISPLAYED_PROFILE_XPATH.format(value))