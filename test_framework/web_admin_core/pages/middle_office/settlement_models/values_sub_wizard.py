from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.middle_office.settlement_models.constants import \
    SettlementModelsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class SettlementModelsValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(SettlementModelsConstants.VALUES_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(SettlementModelsConstants.VALUES_TAB_NAME_XPATH)

    def set_description(self, value):
        self.set_text_by_xpath(SettlementModelsConstants.VALUES_TAB_DESCRIPTION_XPATH, value)

    def get_description(self):
        return self.get_text_by_xpath(SettlementModelsConstants.VALUES_TAB_DESCRIPTION_XPATH)

    def set_settl_location(self, value):
        self.set_combobox_value(SettlementModelsConstants.VALUES_TAB_SETTL_LOCATION_XPATH, value)

    def get_settl_location(self):
        return self.get_text_by_xpath(SettlementModelsConstants.VALUES_TAB_SETTL_LOCATION_XPATH)

    def set_settl_location_bic(self, value):
        self.set_text_by_xpath(SettlementModelsConstants.VALUES_TAB_SETTL_LOCATION_BIC_XPATH, value)

    def get_settl_location_bic(self):
        return self.get_text_by_xpath(SettlementModelsConstants.VALUES_TAB_SETTL_LOCATION_BIC_XPATH)

    def set_instr_type(self, value):
        self.set_combobox_value(SettlementModelsConstants.VALUES_TAB_INSTR_TYPE_XPATH, value)

    def get_instr_type(self):
        return self.get_text_by_xpath(SettlementModelsConstants.VALUES_TAB_INSTR_TYPE_XPATH)

    def set_country_code(self, value):
        self.set_combobox_value(SettlementModelsConstants.VALUES_TAB_COUNTRY_CODE_XPATH, value)

    def get_country_code(self):
        return self.get_text_by_xpath(SettlementModelsConstants.VALUES_TAB_COUNTRY_CODE_XPATH)

    def is_name_field_required(self):
        return self.is_field_required(SettlementModelsConstants.VALUES_TAB_NAME_XPATH)

    def is_description_field_required(self):
        return self.is_field_required(SettlementModelsConstants.VALUES_TAB_DESCRIPTION_XPATH)

    def is_settl_location_field_required(self):
        return self.is_field_required(SettlementModelsConstants.VALUES_TAB_SETTL_LOCATION_XPATH)
