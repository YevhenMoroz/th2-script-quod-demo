import getpass
import random
import string
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import  OrderBookColumns, Side, OrderType, \
    Capacity
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7109(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.bas_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.main_window = BaseMainWindow(self.test_id, self.session_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        self.basket_template_name = "Test Template"
        self.client = "CLIENT_FIX_CARE"
        self.username = getpass.getuser()
        self.path_xlsx = "C:\\Users\\" + self.username + '\\PycharmProjects\\th2-script-quod-demo\\test_cases\\eq\\Basket' \
                                                         '\\Basket_import_files\\BasketTemplate_withHeader_expending_values.xlsx'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region Create basket
        self.bas_book.create_basket_via_import(self.basket_name, self.basket_template_name, self.path_xlsx, self.client)
        order_id1 = self.order_book.set_filter([OrderBookColumns.basket_name.value, self.basket_name]).extract_field(OrderBookColumns.order_id.value)
        order_id2 = self.order_book.set_filter([OrderBookColumns.basket_name.value, self.basket_name]).extract_field(OrderBookColumns.order_id.value, 2)
        # endregion
        # region Check Basket book
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id1]).check_order_fields_list(
            {OrderBookColumns.side.value: Side.sell.value, OrderBookColumns.ord_type.value: OrderType.limit.value,
             OrderBookColumns.capacity.value: Capacity.agency.value})
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id2]).check_order_fields_list(
            {OrderBookColumns.side.value: Side.sell.value, OrderBookColumns.ord_type.value: OrderType.limit.value,
             OrderBookColumns.capacity.value: Capacity.agency.value})
        # endregion
