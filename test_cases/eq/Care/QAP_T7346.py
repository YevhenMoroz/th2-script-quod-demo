import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, PostTradeStatuses, \
    DoneForDays
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7346(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.qty = '300'
        self.qty_to_exec = "200"
        self.price = '30'
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.fix_message.change_parameter('Price', self.price)
        self.client_ord_id_filter = self.fix_message.get_parameter('ClOrdID')


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declarations
        # region create CO
        self.fix_manager.send_message_fix_standard(self.fix_message)
        self.client_inbox.accept_order()
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region manual exec
        self.order_book.manual_execution(qty=self.qty_to_exec, filter_dict={OrderBookColumns.order_id.value: order_id})
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.partially_filled.value})
        # endregion
        # region complete order
        self.order_book.complete_order(filter_list=[OrderBookColumns.order_id.value, order_id])
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value,
             OrderBookColumns.done_for_day.value: DoneForDays.yes.value})
        # endregion
        # region do split and extract error
        self.order_ticket.set_order_details(error_expected=True)
        result = self.order_ticket.split_order(filter_list=[OrderBookColumns.order_id.value, order_id])
        self.order_book.compare_values({f'ErrorMessage': f"Error - [QUOD-24812] Invalid 'DoneForDay': {order_id}"}, result,
                                       'Check error in SplitTicket footer')
        # endregion
