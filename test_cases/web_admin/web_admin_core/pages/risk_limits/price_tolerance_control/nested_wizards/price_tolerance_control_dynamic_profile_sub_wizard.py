from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.risk_limits.price_tolerance_control.price_tolerance_control_constants import \
    PriceToleranceControlConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class PriceToleranceControlDynamicProfileSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark_button(self):
        self.find_by_xpath(PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close_button(self):
        self.find_by_xpath(PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_CLOSE_BUTTON_XPATH).click()

    def click_on_edit_button(self):
        self.find_by_xpath(PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_DELETE_BUTTON_XPATH).click()

    def set_external_price_ctrl_profile_id_filter(self, value):
        self.set_text_by_xpath(
            PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_EXTERNAL_PRICE_CTRL_PROFILE_ID_FILTER_XPATH,
            value)

    def set_external_price_ctrl_profile_id(self, value):
        self.set_text_by_xpath(
            PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_EXTERNAL_PRICE_CTRL_PROFILE_ID_XPATH, value)

    def get_external_price_ctrl_profile_id(self):
        return self.get_text_by_xpath(
            PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_EXTERNAL_PRICE_CTRL_PROFILE_ID_XPATH)

    def set_price_control_type_filter(self, value):
        self.set_text_by_xpath(
            PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_PRICE_CONTROL_TYPE_FILTER_XPATH, value)

    def set_price_control_type(self, value):
        self.set_text_by_xpath(
            PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_PRICE_CONTROL_TYPE_XPATH, value)

    def get_price_control_type(self):
        return self.get_text_by_xpath(
            PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_PRICE_CONTROL_TYPE_XPATH)

    def set_reference_price_type_1_filter(self, value):
        self.set_text_by_xpath(
            PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_1_FILTER_XPATH, value)

    def set_reference_price_type_1(self, value):
        self.set_text_by_xpath(PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_1_XPATH,
                               value)

    def get_reference_price_type_1(self):
        return self.get_text_by_xpath(
            PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_1_XPATH)

    def set_reference_price_type_2_filter(self, value):
        self.set_text_by_xpath(
            PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_2_FILTER_XPATH, value)

    def set_reference_price_type_2(self, value):
        self.set_text_by_xpath(PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_2_XPATH,
                               value)

    def get_reference_price_type_2(self):
        return self.get_text_by_xpath(
            PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_2_XPATH)

    def set_reference_price_type_3_filter(self, value):
        self.set_text_by_xpath(
            PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_3_FILTER_XPATH, value)

    def set_reference_price_type_3(self, value):
        self.set_text_by_xpath(PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_3_XPATH,
                               value)

    def get_reference_price_type_3(self):
        return self.get_text_by_xpath(
            PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_3_XPATH)

    def set_reference_price_type_4_filter(self, value):
        self.set_text_by_xpath(
            PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_4_FILTER_XPATH, value)

    def set_reference_price_type_4(self, value):
        self.set_text_by_xpath(PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_4_XPATH,
                               value)

    def get_reference_price_type_4(self):
        return self.get_text_by_xpath(
            PriceToleranceControlConstants.DYNAMIC_PROFILE_SUB_WIZARD_REFERENCE_PRICE_TYPE_4_XPATH)


