from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.market_making.auto_hedger.auto_hedger_constants import \
    AutoHedgerConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class AutoHedgerValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(AutoHedgerConstants.VALUES_TAB_NAME_FIELD_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(AutoHedgerConstants.VALUES_TAB_NAME_FIELD_XPATH)

    def set_position_book(self, value):
        self.set_combobox_value(AutoHedgerConstants.VALUES_TAB_POSITION_BOOK_FIELD_XPATH, value)

    def get_position_book(self):
        return self.get_text_by_xpath(AutoHedgerConstants.VALUES_TAB_POSITION_BOOK_FIELD_XPATH)
