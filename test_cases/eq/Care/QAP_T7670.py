import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.fix_wrappers.DataSet import Connectivity
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.fe_trading_constant import ExecSts, OrderBookColumns, PostTradeStatuses
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7670(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.order_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.base_window = BaseMainWindow(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.qty2 = str(int(self.qty)+100)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # endregion
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        # endregion
        # region accept CO order
        self.order_inbox.accept_order()
        # endregion
        # region manual execution
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).manual_execution()
        # endregion
        # region check exec status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        # region
        # region amend order by Fix
        fix_message_cancel_replace = FixMessageOrderCancelReplaceRequestOMS(self.data_set)
        fix_message_cancel_replace.set_default(self.fix_message)
        fix_message_cancel_replace.change_parameter('OrderQtyData', {'OrderQty': self.qty2})
        self.fix_manager.send_message_fix_standard(fix_message_cancel_replace)
        # endregion
        # region accept CO order
        self.order_inbox.accept_modify_plus_child()
        # endregion
        # region check qty2
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.qty.value: self.qty2, OrderBookColumns.exec_sts.value: ExecSts.partially_filled.value})
        # endregion
        # region  second manual execution
        OMSOrderBook(self.test_id, self.session_id).set_filter([OrderBookColumns.order_id.value, order_id]).manual_execution()
        # endregion
        # region check qty2
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        # region
        # region complete order
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).complete_order()
        # endregion
        # region check exec status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value})
        # endregion


