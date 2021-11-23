from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.reference_data.listings.listings_constants import ListingsConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingsValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_symbol(self, value):
        self.set_text_by_xpath(ListingsConstants.VALUES_TAB_SYMBOL_XPATH, value)

    def get_symbol(self):
        return self.get_text_by_xpath(ListingsConstants.VALUES_TAB_SYMBOL_XPATH)

    def set_instr_type(self, value):
        self.set_combobox_value(ListingsConstants.VALUES_TAB_INSTR_TYPE_XPATH, value)

    def get_instr_type(self):
        return self.get_text_by_xpath(ListingsConstants.VALUES_TAB_INSTR_TYPE_XPATH)

    def set_security_exchange(self, value):
        self.set_text_by_xpath(ListingsConstants.VALUES_TAB_SECURITY_EXCHANGE_XPATH, value)

    def get_security_exchange(self):
        return self.get_text_by_xpath(ListingsConstants.VALUES_TAB_SECURITY_EXCHANGE_XPATH)

    def set_strike_price(self, value):
        self.set_text_by_xpath(ListingsConstants.VALUES_TAB_STRIKE_PRICE_XPATH, value)

    def get_strike_price(self):
        return self.get_text_by_xpath(ListingsConstants.VALUES_TAB_STRIKE_PRICE_XPATH)

    def set_maturity_date(self, value):
        self.set_text_by_xpath(ListingsConstants.VALUES_TAB_MATURITY_DATE_XPATH, value)

    def get_maturity_date(self):
        return self.get_text_by_xpath(ListingsConstants.VALUES_TAB_MATURITY_DATE_XPATH)

    def set_settl_type(self, value):
        self.set_combobox_value(ListingsConstants.VALUES_TAB_SETTL_TYPE_XPATH, value)

    def get_settl_type(self):
        return self.get_text_by_xpath(ListingsConstants.VALUES_TAB_SETTL_TYPE_XPATH)

    def set_lookup_symbol(self, value):
        self.set_text_by_xpath(ListingsConstants.VALUES_TAB_LOOKUP_SYMBOL_XPATH, value)

    def get_lookup_symbol(self):
        return self.get_text_by_xpath(ListingsConstants.VALUES_TAB_LOOKUP_SYMBOL_XPATH)

    def set_instr_sub_type(self, value):
        self.set_combobox_value(ListingsConstants.VALUES_TAB_INSTR_SUB_TYPE_XPATH, value)

    def get_instr_sub_type(self):
        return self.get_text_by_xpath(ListingsConstants.VALUES_TAB_INSTR_SUB_TYPE_XPATH)

    def set_preferred_security_exchange(self, value):
        self.set_text_by_xpath(ListingsConstants.VALUES_TAB_PREFERRED_SECURITY_EXCHANGE_XPATH, value)

    def get_preferred_security_exchange(self):
        return self.get_text_by_xpath(ListingsConstants.VALUES_TAB_PREFERRED_SECURITY_EXCHANGE_XPATH)

    def set_tenor(self, value):
        self.set_combobox_value(ListingsConstants.VALUES_TAB_TENOR_XPATH, value)

    def get_tenor(self):
        return self.get_text_by_xpath(ListingsConstants.VALUES_TAB_TENOR_XPATH)

    def set_maturity_month_year(self, value):
        self.set_text_by_xpath(ListingsConstants.VALUES_TAB_MATURITY_MONTH_YEAR_XPATH, value)

    def get_maturity_month_year(self):
        return self.get_text_by_xpath(ListingsConstants.VALUES_TAB_MATURITY_MONTH_YEAR_XPATH)

    def click_on_dummy(self):
        self.find_by_xpath(ListingsConstants.VALUES_TAB_DUMMY_CHECKBOX_XPATH).click()

    def set_instr_symbol(self, value):
        self.set_text_by_xpath(ListingsConstants.VALUES_TAB_INSTR_SYMBOL_XPATH, value)

    def get_instr_symbol(self):
        return self.get_text_by_xpath(ListingsConstants.VALUES_TAB_INSTR_SYMBOL_XPATH)

    def set_cfi(self, value):
        self.set_text_by_xpath(ListingsConstants.VALUES_TAB_CFI_XPATH, value)

    def get_cfi(self):
        return self.get_text_by_xpath(ListingsConstants.VALUES_TAB_CFI_XPATH)

    def set_mic(self, value):
        self.set_text_by_xpath(ListingsConstants.VALUES_TAB_MIC_XPATH, value)

    def get_mic(self):
        return self.get_text_by_xpath(ListingsConstants.VALUES_TAB_MIC_XPATH)

    def set_call_put(self, value):
        self.set_combobox_value(ListingsConstants.VALUES_TAB_CALL_PUT_XPATH, value)

    def get_call_put(self):
        return self.get_text_by_xpath(ListingsConstants.VALUES_TAB_CALL_PUT_XPATH)

    def set_instr_settl_date(self, value):
        self.set_text_by_xpath(ListingsConstants.VALUES_TAB_INSTR_SETTL_DATE_XPATH, value)

    def get_instr_settl_date(self):
        return self.get_text_by_xpath(ListingsConstants.VALUES_TAB_INSTR_SETTL_DATE_XPATH)

    def is_tenor_field_required(self):
        return "ng-invalid" in self.find_by_xpath(ListingsConstants.VALUES_TAB_TENOR_XPATH).get_attribute("class")

    def is_maturity_month_year_field_required(self):
        return "ng-invalid" in self.find_by_xpath(ListingsConstants.VALUES_TAB_MATURITY_MONTH_YEAR_XPATH).get_attribute("class")

    def is_strike_price_field_required(self):
        return "ng-invalid" in self.find_by_xpath(ListingsConstants.VALUES_TAB_STRIKE_PRICE_XPATH).get_attribute(
            "class")

    def is_call_put_field_required(self):
        return "ng-invalid" in self.find_by_xpath(ListingsConstants.VALUES_TAB_CALL_PUT_XPATH).get_attribute(
            "class")