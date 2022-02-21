import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_trading.web_trading_core.pages.main_page.workspace.order_book.order_book_constants import \
    OrderBookConstants


class OrderBookPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # region Filter values in main page
    def get_symbol(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_SYMBOL_XPATH).text

    def get_instr_type(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_INSTR_TYPE_XPATH).text

    def get_order_id(self):
        pass

    def get_account_code(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_ACCOUNT_CODE_XPATH).text

    def get_side(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_SIDE_XPATH).text

    def get_order_qty(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_ORDER_QTY_XPATH).text

    def get_price(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_PRICE_XPATH).text

    def get_avg_price(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_AVG_PRICE_XPATH).text

    def get_leaves_qty(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_LEAVES_QTY_XPATH).text

    def get_order_type(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_ORDER_TYPE_XPATH).text

    def get_cum_qty(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_CUM_QTY_XPATH).text

    def get_order_status(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_ORDER_STATUS_XPATH).text

    def get_expire_date(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_EXPIRE_DATE_XPATH).text

    def get_settle_date(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_SETTLE_DATE_XPATH).text

    def get_settle_type(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_SETTLE_TYPE_XPATH).text

    def get_time_in_force(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_TIME_IN_FORCE_XPATH).text

    def get_free_notes(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_FREE_NOTES_XPATH).text

    def get_account(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_ACCOUNT_XPATH).text

    def get_transaction_time(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_TRANSACTION_TIME_XPATH).text

    def get_cl_ord_id(self):
        return self.find_by_xpath(OrderBookConstants.ORDER_CIORDID_XPATH).text

    # endregion

    def click_on_field_chooser_button(self):
        self.find_by_xpath(OrderBookConstants.FIELD_CHOOSER_XPATH).click()

    def select_visible_columns(self, value):
        self.set_checkbox_list(OrderBookConstants.LIST_CHECKBOX_XPATH, value)

    def click_on_hide_all(self):
        self.find_by_xpath(OrderBookConstants.HIDE_ALL_BUTTON_XPATH).click()

    def click_on_show_all(self):
        self.find_by_xpath(OrderBookConstants.SHOW_ALL_BUTTON_XPATH).click()

    # region order filter switch
    def click_on_switch_at_order_filter(self):
        self.find_by_xpath(OrderBookConstants.SWITCH_BUTTON_XPATH).click()

    def set_from_date(self, date):
        self.set_text_by_xpath(OrderBookConstants.FROM_FIELD_XPATH, date)

    def set_to_date(self, date):
        self.set_text_by_xpath(OrderBookConstants.TO_FIELD_XPATH, date)

    def click_on_search_button(self):
        self.find_by_xpath(OrderBookConstants.SEARCH_XPATH).click()

    # endregion

    # region Auxiliary menu on the symbol

    def click_on_buy_button(self):
        self.find_by_xpath(OrderBookConstants.BUY_HOVER_BUTTON_XPATH).click()

    def click_on_sell_button(self):
        self.find_by_xpath(OrderBookConstants.SELL_HOVER_BUTTON_XPATH).click()

    def click_on_modify_button(self):
        self.find_by_xpath(OrderBookConstants.MODIFY_HOVER_BUTTON_XPATH).click()

    def click_on_market_depth_button(self):
        self.find_by_xpath(OrderBookConstants.MARKET_DEPTH_HOVER_BUTTON_XPATH).click()

    def click_on_times_and_sales_button(self):
        self.find_by_xpath(OrderBookConstants.TIMES_AND_SALES_HOVER_BUTTON_XPATH).click()

    def click_on_order_cancel_button(self):
        self.find_by_xpath(OrderBookConstants.CANCEL_HOVER_BUTTON_XPATH).click()

    def click_on_re_order_button(self):
        self.find_by_xpath(OrderBookConstants.REORDER_HOVER_BUTTON_XPATH).click()
# endregion

    def click_on_copy_panel(self):
        self.find_by_xpath(OrderBookConstants.COPY_PANEL_BUTTON_XPATH).click()

    def click_on_maximize_button(self):
        self.find_element_in_shadow_root(OrderBookConstants.MAXIMIZE_BUTTON_CSS)

    def click_on_minimize_button(self):
        self.find_element_in_shadow_root(OrderBookConstants.MINIMIZE_BUTTON_CSS)

    def click_on_close_order_book_wizard(self):
        self.find_element_in_shadow_root(OrderBookConstants.CLOSE_BUTTON_CSS)

    def check_order(self):
        return self.get_symbol(), self.get_account(), self.get_side(), self.get_order_qty(), self.get_price(), self.get_order_type()

    #region Filter Column Buttons

    def click_on_filter_order_id_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_ORDER_ID_COLUMN_XPATH).click()

    def click_on_filter_symbol_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_SYMBOL_COLUMN_XPATH).click()

    def click_on_filter_instr_type_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_INSTR_TYPE_COLUMN_XPATH).click()

    def click_on_filter_account_code_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_ACCOUNT_CODE_COLUMN_XPATH).click()

    def click_on_filter_side_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_SIDE_COLUMN_XPATH).click()

    def click_on_filter_order_qty_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_ORDER_QTY_COLUMN_XPATH).click()

    def click_on_filter_price_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_PRICE_COLUMN_XPATH).click()

    def click_on_filter_avg_price_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_AVG_PRICE_COLUMN_XPATH).click()

    def click_on_filter_leaves_qty_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_LEAVES_QTY_COLUMN_XPATH).click()

    def click_on_filter_order_type_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_ORDER_TYPE_COLUMN_XPATH).click()

    def click_on_filter_cum_qty_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_CUM_QTY_COLUMN_XPATH).click()

    def click_on_filter_order_status_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_ORDER_STATUS_COLUMN_XPATH).click()

    def click_on_filter_expire_date_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_EXPIRE_DATE_COLUMN_XPATH).click()

    def click_on_filter_settle_date_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_SETTLE_DATE_COLUMN_XPATH).click()

    def click_on_filter_settle_type_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_SETTLE_TYPE_COLUMN_XPATH).click()

    def click_on_filter_time_in_force_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_TIME_IN_FORCE_COLUMN_XPATH).click()

    def click_on_filter_free_notes_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_FREE_NOTES_COLUMN_XPATH).click()

    def click_on_filter_account_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_ACCOUNT_COLUMN_XPATH).click()

    def click_on_filter_transaction_time_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_TRANSACTION_TIME_COLUMN_XPATH).click()

    def click_on_filter_ciordid_button(self):
        self.find_by_xpath(OrderBookConstants.FILTER_CIORDID_COLUMN_XPATH).click()

    #endregion

    #region Filter

    def set_search_field(self, order_id):
        self.set_text_by_xpath(OrderBookConstants.SEARCH_FIELD_XPATH, order_id)

    def click_on_apply_button(self):
        self.find_by_xpath(OrderBookConstants.APPLY_BUTTON_XPATH).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(OrderBookConstants.APPLY_BUTTON_XPATH).click()

    #endregion