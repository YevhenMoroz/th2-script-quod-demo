import random
import string
import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.win_gui_wrappers.fe_trading_constant import BasketBookColumns, TimeInForce, OrderBookColumns, \
    ExecSts, PostTradeStatuses
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

import getpass

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7408(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        self.username = getpass.getuser()
        self.client = self.data_set.get_client_by_name('client_pos_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.path_csv = "C:\\Users\\" + self.username + '\\PycharmProjects\\th2-script-quod-demo\\test_cases\\eq\\Basket' \
                                                        '\\Basket_import_files\\BasketTemplate_withHeader_Mapping2.csv'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create basket via template csv
        self.basket_book.create_basket_via_import(basket_name=self.basket_name,
                                                  basket_template_name="Test Template",
                                                  path=self.path_csv, client=self.client, tif=TimeInForce.DAY.value,
                                                  is_csv=True)
        basket_id = self.basket_book.get_basket_value(BasketBookColumns.id.value)
        order_id1 = self.order_book.set_filter([OrderBookColumns.basket_name.value, self.basket_name]).extract_field(
            OrderBookColumns.order_id.value, row_number=1)
        order_id2 = self.order_book.set_filter([OrderBookColumns.basket_name.value, self.basket_name]).extract_field(
            OrderBookColumns.order_id.value, row_number=2)
        # endregion
        # region manual exec orders
        self.order_book.manual_execution(filter_dict={OrderBookColumns.order_id.value: order_id1})
        self.order_book.manual_execution(filter_dict={OrderBookColumns.order_id.value: order_id2})
        # endregion
        # region check fields
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id1]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id2]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        # endregion
        # region complete orders
        self.basket_book.complete_basket({BasketBookColumns.id.value: basket_id})
        # endregion
        # region check fields
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id1]).check_order_fields_list(
            {OrderBookColumns.done_for_day.value: "Yes",
             OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value})
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id2]).check_order_fields_list(
            {OrderBookColumns.done_for_day.value: "Yes",
             OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value})
        # endregion
        # region book basket
        self.basket_book.book_basket()
        # endregion
        # region check fields
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id1]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value})
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id2]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value})
        # endregion
