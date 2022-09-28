import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, TimeInForce, \
    PostTradeStatuses
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True



class QAP_T7515(TestCase):


    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.qty1 = "100"
        self.qty2 = "70"
        self.qty3 = "30"
        self.price = "5"
        self.price2 = "7"
        self.last_mkt = "BAML"
        self.fix_message1 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_market()
        self.fix_message1.change_parameter('OrderQtyData', {'OrderQty': self.qty1})
        self.fix_message2 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_market()
        self.fix_message2.change_parameter('OrderQtyData', {'OrderQty': self.qty2})
        self.fix_message2.change_parameter("Side", "2")
        self.fix_message3 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_market()
        self.fix_message3.change_parameter('OrderQtyData', {'OrderQty': self.qty3})
        self.fix_message3.change_parameter("Side", "2")
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.cl_ord_id = self.fix_message1.get_parameter('ClOrdID')
        self.rule_manager = RuleManager()




    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create CO1 order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message1)
        order_id1 = response[0].get_parameters()['OrderID']
        # endregion
        # region accept first order
        self.client_inbox.accept_order()
        # endregion
        # region create CO2 order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message2)
        order_id2 = response[0].get_parameters()['OrderID']
        # endregion
        # region accept second order
        self.client_inbox.accept_order()
        # endregion
        # region create CO3 order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message3)
        order_id3 = response[0].get_parameters()['OrderID']
        # endregion
        # region accept third order
        self.client_inbox.accept_order()
        # endregion
        # region man cross CO1 and CO2
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, self.cl_ord_id[:-1]]).manual_cross_orders([3,2], self.qty2, self.price, self.last_mkt)
        # endregion
        # region check partially filled CO1 status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id1]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.partially_filled.value})
        # endregion
        # region check filled CO2 status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id2]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        # endregion
        # region man cross CO1 and CO3
        self.order_book.manual_cross_orders([2, 1], self.qty3, self.price2, self.last_mkt)
        # endregion
        # region check filled CO1 status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id1]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        # endregion
        # region check filled CO3 status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id3]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        # endregion
