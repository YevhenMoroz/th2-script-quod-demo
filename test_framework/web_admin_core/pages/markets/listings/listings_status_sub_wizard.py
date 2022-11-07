from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.listings.listings_constants import \
    ListingsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingsStatusSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_trading_phase(self, value):
        self.set_combobox_value(ListingsConstants.STATUS_TAB_TRADING_PHASE_XPATH, value)

    def get_trading_phase(self):
        return self.get_text_by_xpath(ListingsConstants.STATUS_TAB_TRADING_PHASE_XPATH)

    def set_trading_session(self, value):
        self.set_text_by_xpath(ListingsConstants.STATUS_TAB_TRADING_SESSION_XPATH, value)

    def get_trading_session(self):
        return self.get_text_by_xpath(ListingsConstants.STATUS_TAB_TRADING_SESSION_XPATH)

    def set_trading_status(self, value):
        self.set_combobox_value(ListingsConstants.STATUS_TAB_TRADING_STATUS_XPATH, value)

    def get_trading_status(self):
        return self.get_text_by_xpath(ListingsConstants.STATUS_TAB_TRADING_STATUS_XPATH)

    def set_external_trading_status(self, value):
        self.set_combobox_value(ListingsConstants.STATUS_TAB_EXTERNAL_TRADING_STATUS_PHASE_XPATH, value)

    def get_external_trading_status(self):
        return self.get_text_by_xpath(ListingsConstants.STATUS_TAB_EXTERNAL_TRADING_STATUS_PHASE_XPATH)
