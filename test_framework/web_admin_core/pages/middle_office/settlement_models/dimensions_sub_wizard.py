from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.middle_office.settlement_models.constants import \
    SettlementModelsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class SettlementModelsDimensionsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_client_group(self, value):
        self.set_combobox_value(SettlementModelsConstants.DIMENSIONS_TAB_CLIENT_GROUP_XPATH, value)

    def get_client_group(self):
        return self.get_text_by_xpath(SettlementModelsConstants.DIMENSIONS_TAB_CLIENT_GROUP_XPATH)

    def set_account(self, value):
        self.set_combobox_value(SettlementModelsConstants.DIMENSIONS_TAB_ACCOUNT_XPATH, value)

    def get_account(self):
        return self.get_text_by_xpath(SettlementModelsConstants.DIMENSIONS_TAB_ACCOUNT_XPATH)

    def set_client(self, value):
        self.set_combobox_value(SettlementModelsConstants.DIMENSIONS_TAB_CLIENT_XPATH, value)

    def get_client(self):
        return self.get_text_by_xpath(SettlementModelsConstants.DIMENSIONS_TAB_CLIENT_XPATH)

    def set_venue(self, value):
        self.set_combobox_value(SettlementModelsConstants.DIMENSIONS_TAB_VENUE_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(SettlementModelsConstants.DIMENSIONS_TAB_VENUE_XPATH)

    def set_instrument(self, value):
        self.set_combobox_value(SettlementModelsConstants.DIMENSIONS_TAB_INSTRUMENT_XPATH, value)

    def get_instrument(self):
        return self.get_text_by_xpath(SettlementModelsConstants.DIMENSIONS_TAB_INSTRUMENT_XPATH)

    def set_instrument_group(self, value):
        self.set_combobox_value(SettlementModelsConstants.DIMENSIONS_TAB_INSTRUMENT_GROUP_XPATH, value)

    def get_instrument_group(self):
        return self.get_text_by_xpath(SettlementModelsConstants.DIMENSIONS_TAB_INSTRUMENT_GROUP_XPATH)
