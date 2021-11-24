from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.risk_limits.price_tolerance_control.price_tolerance_control_constants import \
    PriceToleranceControlConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class PriceToleranceControlOrdrSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(PriceToleranceControlConstants.ORDR_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark_button(self):
        self.find_by_xpath(PriceToleranceControlConstants.ORDR_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close_button(self):
        self.find_by_xpath(PriceToleranceControlConstants.ORDR_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit_button(self):
        self.find_by_xpath(PriceToleranceControlConstants.ORDR_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(PriceToleranceControlConstants.ORDR_TAB_DELETE_BUTTON_XPATH).click()

    def set_ord_type(self,value):
        self.set_combobox_value(PriceToleranceControlConstants.ORDR_TAB_ORD_TYPE_XPATH,value)

    def get_ord_type(self):
        return self.get_text_by_xpath(PriceToleranceControlConstants.ORDR_TAB_ORD_TYPE_XPATH)

    def set_ord_type_filter(self,value):
        self.set_text_by_xpath(PriceToleranceControlConstants.ORDR_TAB_ORD_TYPE_FILTER_XPATH,value)

    def set_side(self,value):
        self.set_combobox_value(PriceToleranceControlConstants.ORDR_TAB_SIDE_XPATH,value)

    def get_side(self):
        return self.get_text_by_xpath(PriceToleranceControlConstants.ORDR_TAB_SIDE_XPATH)

    def set_trading_phase(self,value):
        self.set_combobox_value(PriceToleranceControlConstants.ORDR_TAB_TRADING_PHASE_XPATH,value)

    def get_trading_phase(self):
        return self.get_text_by_xpath(PriceToleranceControlConstants.ORDR_TAB_TRADING_PHASE_XPATH)

    def set_max_qty_adv(self,value):
        self.set_text_by_xpath(PriceToleranceControlConstants.ORDR_TAB_MAX_QTY_ADV_XPATH,value)

    def get_max_qty_adv(self):
        return self.get_text_by_xpath(PriceToleranceControlConstants.ORDR_TAB_MAX_QTY_ADV_XPATH)

    def click_on_aggressor_indicator_checkbox(self):
        self.find_by_xpath(PriceToleranceControlConstants.ORDR_TAB_AGGRESSOR_INDICATOR_XPATH).click()

    def  set_static_profile(self,value):
        self.set_combobox_value(PriceToleranceControlConstants.ORDR_TAB_STATIC_PROFILE_XPATH,value)

    def get_static_profile(self):
        return self.get_text_by_xpath(PriceToleranceControlConstants.ORDR_TAB_STATIC_PROFILE_XPATH)

    def set_dynamic_profile(self,value):
        self.set_text_by_xpath(PriceToleranceControlConstants.ORDR_TAB_DYNAMIC_PROFILE_XPATH,value)

    def get_dynamic_profile(self):
        return self.get_text_by_xpath(PriceToleranceControlConstants.ORDR_TAB_DYNAMIC_PROFILE_XPATH)

    def click_on_manage_dynamic_profile(self):
        self.find_by_xpath(PriceToleranceControlConstants.ORDR_TAB_DYNAMIC_PROFILE_MANAGE_BUTTON_XPATH).click()















































