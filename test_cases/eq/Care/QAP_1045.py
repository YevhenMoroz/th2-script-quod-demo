import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.DataSet import Connectivity
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelRequestOMS import FixMessageOrderCancelRequestOMS
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_1045(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.lookup = "VETO"
        self.qty2 = "1000"
        self.price2 = "35"
        self.ss_connectivity = Connectivity.Ganymede_317_ss.value
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.base_window = BaseMainWindow(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region accept CO order
        self.client_inbox.accept_order('O', 'M', 'S')
        # endregion
        # region compare values 1
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion
        # region amend order via FIX
        fix_message_cancel_replace = FixMessageOrderCancelReplaceRequestOMS(self.data_set)
        fix_message_cancel_replace.set_default(self.fix_message)
        fix_message_cancel_replace.change_parameter('OrderQtyData', {'OrderQty': self.qty2})
        fix_message_cancel_replace.change_parameter("Price", self.price2)
        self.fix_manager.send_message_fix_standard(fix_message_cancel_replace)
        # endregion
        # region check accept modify
        self.client_inbox.accept_modify_plus_child(self.lookup, self.qty2, self.price2)
        # endregion
        # region check changed values
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.qty.value: self.qty2, OrderBookColumns.limit_price.value: self.price2})
        # endregion
        # region cancel order via FIX
        fix_message_cancel = FixMessageOrderCancelRequestOMS()
        fix_message_cancel.set_default(self.fix_message)
        self.fix_manager.send_message_fix_standard(fix_message_cancel)
        # endregion
        # region accept cancel
        self.client_inbox.accept_and_cancel_children(self.lookup, self.qty2, self.price2)
        # endregion
        # region check cancelled status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.cancelled.value})
        # endregion


