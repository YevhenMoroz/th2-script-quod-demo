from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_trading.web_trading_core.pages.main_page.workspace.trades.trades_constants import \
    TradesConstants


class TradesPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # TODO: implement methods, if something changed in FE part, please take a look

    # region Filter values in main page

    def get_symbol(self):
        return self.find_by_xpath(TradesConstants.ORDER_SYMBOL_XPATH).text

    def get_instr_type(self):
        return self.find_by_xpath(TradesConstants.ORDER_INSTR_TYPE_XPATH).text

    def get_order_id(self):
        return self.find_by_xpath(TradesConstants.ORDER_ORDER_ID_XPATH).text

    def get_excel_id(self):
        return self.find_by_xpath(TradesConstants.ORDER_EXCEL_ID_XPATH).text

    def get_side(self):
        return self.find_by_xpath(TradesConstants.ORDER_SIDE_XPATH).text

    def get_qty(self):
        return self.find_by_xpath(TradesConstants.ORDER_QTY_XPATH).text

    def get_execution_price(self):
        return self.find_by_xpath(TradesConstants.ORDER_EXECUTION_PRICE_XPATH).text

    def get_execution_type(self):
        return self.find_by_xpath(TradesConstants.ORDER_EXECUTION_TYPE_XPATH).text

    def get_avg_price(self):
        return self.find_by_xpath(TradesConstants.ORDER_AVG_PRICE_XPATH).text

    def get_cumulative_qty(self):
        return self.find_by_xpath(TradesConstants.ORDER_CUMULATIVE_QTY_XPATH).text

    def get_leaves_qty(self):
        return self.find_by_xpath(TradesConstants.ORDER_LEAVES_QTY_XPATH).text

    def get_order_status(self):
        return self.find_by_xpath(TradesConstants.ORDER_ORDER_STATUS_XPATH).text

    def get_transaction_time(self):
        return self.find_by_xpath(TradesConstants.ORDER_TRANSACTION_TIME_XPATH).text

    # endregion

    # region Visible columns
    def click_on_field_chooser_button(self):
        self.find_by_xpath(TradesConstants.FIELD_CHOOSER_XPATH).click()

    def select_visible_columns(self, value):
        self.set_checkbox_list(TradesConstants.LIST_CHECKBOX_XPATH, value)

    def click_on_hide_all(self):
        self.find_by_xpath(TradesConstants.HIDE_ALL_BUTTON_XPATH).click()

    def click_on_show_all(self):
        self.find_by_xpath(TradesConstants.SHOW_ALL_BUTTON_XPATH).click()

    # endregion

    # region Advanced filtering
    def click_on_advanced_filtering_button(self):
        self.find_by_xpath(TradesConstants.ADVANCED_FILTERING_BUTTON_XPATH).click()

    # endregion

    def click_on_copy_panel_button(self):
        self.find_by_xpath(TradesConstants.COPY_PANEL_BUTTON_XPATH).click()

    def click_on_maximize_button(self):
        self.find_element_in_shadow_root(TradesConstants.MAXIMIZE_BUTTON_CSS)

    def click_on_minimize_button(self):
        self.find_element_in_shadow_root(TradesConstants.MINIMIZE_BUTTON_CSS)

    def click_on_close_trades_button(self):
        self.find_element_in_shadow_root(TradesConstants.CLOSE_BUTTON_CSS)

    # region Auxiliary menu on the symbol

    def click_on_buy_button(self):
        self.find_by_xpath(TradesConstants.BUY_HOVER_BUTTON_XPATH).click()

    def click_on_sell_button(self):
        self.find_by_xpath(TradesConstants.SELL_HOVER_BUTTON_XPATH).click()

    def click_on_market_depth_button(self):
        self.find_by_xpath(TradesConstants.MARKET_DEPTH_HOVER_BUTTON_XPATH).click()

    def click_on_times_and_sales_button(self):
        self.find_by_xpath(TradesConstants.TIMES_AND_SALES_HOVER_BUTTON_XPATH).click()
# endregion
