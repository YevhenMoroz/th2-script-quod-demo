import random
import string
import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.win_gui_wrappers.fe_trading_constant import BasketBookColumns, TimeInForce, Side, OrderType, \
    OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
import getpass

from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7441(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        self.username = getpass.getuser()
        self.new_symbol = "FR0004186856"
        self.new_qty = "500"
        self.new_price = "0"
        self.new_capacity = "Principal"
        self.client = self.data_set.get_client_by_name('client_pos_1')
        self.path_csv = "C:\\Users\\" + self.username + '\\PycharmProjects\\th2-script-quod-demo\\test_cases\\eq\\Basket' \
                                              '\\Basket_import_files\\BasketTemplate_withHeader_Mapping1.csv'


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create basket via template csv
        details = self.basket_book.basket_row_details(symbol=self.new_symbol, side=Side.buy.value,
                                            qty=self.new_qty, ord_type=OrderType.market.value,price = self.new_price,
                                            capacity=self.new_capacity)
        self.basket_book.create_basket_via_import(basket_name=self.basket_name,
                                                  basket_template_name="Test Template",
                                                  path=self.path_csv, client=self.client, tif=TimeInForce.DAY.value,
                                                  is_csv=True, amend_rows_details=[details])
        order_id = self.order_book.set_filter([OrderBookColumns.basket_name.value, self.basket_name]).extract_field(
            OrderBookColumns.order_id.value, 2)
        # endregion
        # region check basket fields
        self.basket_book.check_basket_field(BasketBookColumns.exec_policy.value, "Care")
        self.basket_book.check_basket_field(BasketBookColumns.status.value, "Executing")
        self.basket_book.check_basket_field(BasketBookColumns.list_exec_inst_type.value, "Immediate")
        self.basket_book.check_basket_field(BasketBookColumns.basket_name.value, self.basket_name)
        # endregion
        # region check order fields
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.basket_name.value: self.basket_name, OrderBookColumns.qty.value: self.new_qty,
             OrderBookColumns.limit_price.value: "", OrderBookColumns.ord_type.value: OrderType.market.value})
        # endregion


