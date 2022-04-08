from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_trading.web_trading_core.pages.main_page.workspace.symbol_details.symbol_details_constants import \
    SymbolsDetailsConstants


class SymbolDetailsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # Set symbol in the search symbol field
    def set_symbol(self, symbol):
        self.set_combobox_value(SymbolsDetailsConstants.SEARCH_SYMBOL_INPUT_FIELD_XPATH, symbol)
