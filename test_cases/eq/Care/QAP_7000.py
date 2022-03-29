import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, OrderType
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_7000(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.username = environment.get_list_fe_environment()[0].user_1
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.order_type = OrderType.limit.value
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        nos = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_manager.send_message_fix_standard(nos)

        cl_ord_id = nos.get_parameter('ClOrdID')
        qty = nos.get_parameter('OrderQtyData')["OrderQty"]
        price = nos.get_parameter('Price')

        self.client_inbox.accept_order(filter={"ClOrdId": cl_ord_id})

        exp_day_cum_qty = qty
        exp_day_cum_amt = str(int(int(qty) * int(price)))

        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.open.value})

        self.order_book.manual_execution(filter_dict={OrderBookColumns.cl_ord_id.value: cl_ord_id})

        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id]).check_order_fields_list(
            {OrderBookColumns.day_cum_qty.value: exp_day_cum_qty, OrderBookColumns.day_cum_amt.value: exp_day_cum_amt})

        self.order_book.complete_order(1, [OrderBookColumns.cl_ord_id.value, cl_ord_id])

        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id]).check_order_fields_list(
            {OrderBookColumns.day_cum_qty.value: exp_day_cum_qty, OrderBookColumns.day_cum_amt.value: exp_day_cum_amt})

        self.order_book.un_complete_order(1, [OrderBookColumns.cl_ord_id.value, cl_ord_id])

        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id]).check_order_fields_list(
            {OrderBookColumns.day_cum_qty.value: exp_day_cum_qty, OrderBookColumns.day_cum_amt.value: exp_day_cum_amt})


