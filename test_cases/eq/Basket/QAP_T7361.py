import getpass
import logging
import os
import random
import string
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import TimeInForce, OrderBookColumns, BasketBookColumns
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7361(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        self.username = getpass.getuser()
        self.client = self.data_set.get_client_by_name('client_co_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.path_xlsx = "C:\\Users\\" + self.username + '\\PycharmProjects\\th2-script-quod-demo\\test_cases\\eq\\Basket' \
                                                         '\\Basket_import_files\\testDummyValues2.xlsx'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create basket via template xlsx
        result_expected = self.basket_book.basket_row_details(row_filter='100', remove_row=True)
        self.basket_book.create_basket_via_import(basket_name=self.basket_name,
                                                  basket_template_name="Test Template",
                                                  path=self.path_xlsx, client=self.client, tif=TimeInForce.DAY.value,
                                                  amend_rows_details=[result_expected])
        # endregion
        # region check values
        result1 = self.basket_book.get_basket_sub_lvl_value(1, OrderBookColumns.qty.value,
                                                            BasketBookColumns.orders_tab.value,
                                                            basket_book_filter={
                                                                BasketBookColumns.basket_name.value: self.basket_name})
        expected = {'1': '200'}
        self.basket_book.compare_values(expected, result1, 'Check Qty')
        result2 = self.basket_book.get_basket_sub_lvl_value(2, OrderBookColumns.qty.value,
                                                            BasketBookColumns.orders_tab.value,
                                                            basket_book_filter={
                                                                BasketBookColumns.basket_name.value: self.basket_name})
        expected = {'2': '300'}
        self.basket_book.compare_values(expected, result2, 'Check Qty')
        # endregion
