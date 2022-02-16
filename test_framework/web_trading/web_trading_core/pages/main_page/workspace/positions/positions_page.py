from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_trading.web_trading_core.pages.main_page.workspace.positions.positions_constants import \
    PositionsConstants


class PositionsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # TODO: implement methods, if something changed in FE part, please take a look
    # region Filter values in main page
    def get_symbol(self):
        return self.find_by_xpath(PositionsConstants.ORDER_SYMBOL_XPATH).text

    def get_instr_type(self):
        return self.find_by_xpath(PositionsConstants.ORDER_INSTR_TYPE_XPATH).text

    def get_exchange(self):
        return self.find_by_xpath(PositionsConstants.ORDER_EXCHANGE_XPATH).text

    def get_total_qty(self):
        return self.find_by_xpath(PositionsConstants.ORDER_TOTAL_QTY_XPATH).text

    def get_reserved_qty(self):
        return self.find_by_xpath(PositionsConstants.ORDER_RESERVED_QTY_XPATH).text

    def get_covered_qty(self):
        return self.find_by_xpath(PositionsConstants.ORDER_COVERED_QTY_XPATH).text

    def get_leaves_buy_qty(self):
        return self.find_by_xpath(PositionsConstants.ORDER_LEAVES_BUY_QTY_XPATH).text

    def get_leaves_sell_qty(self):
        return self.find_by_xpath(PositionsConstants.ORDER_LEAVES_SELL_QTY_XPATH).text

    def get_cumulative_buy_amt(self):
        return self.find_by_xpath(PositionsConstants.ORDER_CUMULATIVE_BUY_AMT_XPATH).text

    def get_cumulative_sell_amt(self):
        return self.find_by_xpath(PositionsConstants.ORDER_CUMULATIVE_SELL_AMT_XPATH).text

    # endregion

    # region Visible columns
    def click_on_field_chooser_button(self):
        self.find_by_xpath(PositionsConstants.FIELD_CHOOSER_XPATH).click()

    def select_visible_columns(self, value):
        self.set_checkbox_list(PositionsConstants.LIST_CHECKBOX_XPATH, value)

    def click_on_hide_all(self):
        self.find_by_xpath(PositionsConstants.HIDE_ALL_BUTTON_XPATH).click()

    def click_on_show_all(self):
        self.find_by_xpath(PositionsConstants.SHOW_ALL_BUTTON_XPATH).click()

    # endregion

    # region Advanced filtering
    def click_on_advanced_filtering_button(self):
        self.find_by_xpath(PositionsConstants.ADVANCED_FILTERING_BUTTON_XPATH).click()

    # endregion

    def click_on_copy_panel(self):
        self.find_by_xpath(PositionsConstants.COPY_PANEL_BUTTON_XPATH).click()

    def click_on_maximize_button(self):
        self.find_element_in_shadow_root(PositionsConstants.MAXIMIZE_BUTTON_CSS)

    def click_on_minimize_button(self):
        self.find_element_in_shadow_root(PositionsConstants.MINIMIZE_BUTTON_CSS)

    def click_on_close_positions_wizard(self):
        self.find_element_in_shadow_root(PositionsConstants.CLOSE_BUTTON_CSS)
