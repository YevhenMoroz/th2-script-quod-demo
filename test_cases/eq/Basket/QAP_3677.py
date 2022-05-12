import random
import string
import logging
from datetime import datetime, timedelta
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, BasketBookColumns
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_3677(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.qty = "900"
        self.price = "20"
        self.last_capacity = "Agency"
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.fix_message.change_parameter("Price", self.price)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        self.cl_ord_id = self.fix_message.get_parameter('ClOrdID')


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create first CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        order_id1 = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region create second CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        order_id2 = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region accept CO order
        self.client_inbox.accept_order()
        self.client_inbox.accept_order()
        # endregion
        # region create basket
        self.order_book.create_basket(orders_rows=[1, 2], basket_name=self.basket_name)
        # endregion
        # region get basket id
        basket_id = self.basket_book.get_basket_value(BasketBookColumns.id.value)
        # endregion
        # check basket fields
        self.basket_book.check_basket_field(BasketBookColumns.exec_policy.value, "Care")
        self.basket_book.check_basket_field(BasketBookColumns.status.value, "Executing")
        self.basket_book.check_basket_field(BasketBookColumns.basket_name.value, self.basket_name)
        # endregion
        # check basket 2nd level fields
        # self.basket_book.check_basket_sub_lvl_field(1,  "Sts", "Orders", ExecSts.open.value)
        # self.basket_book.check_basket_sub_lvl_field(2,  "Sts", "Orders", ExecSts.open.value)
        # endregion
        # check order in Order Book
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id1]).check_order_fields_list(
            {OrderBookColumns.basket_name.value: self.basket_name, OrderBookColumns.basket_id.value: basket_id})
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id2]).check_order_fields_list(
            {OrderBookColumns.basket_name.value: self.basket_name, OrderBookColumns.basket_id.value: basket_id})
        # endregion


