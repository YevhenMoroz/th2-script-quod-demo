import logging

from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import  OrderBookColumns,  OrderType
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True



@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7677(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty_to_split = "50"
        self.qty_to_display = "25"
        self.order_type = OrderType.limit.value
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.client = self.data_set.get_client_by_name('client_co_1')
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send Fix Message
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        # endregion
        # region Accept
        self.client_inbox.accept_order()
        # endregion
        # region Split
        self.order_ticket.set_order_details(qty=self.qty_to_split)
        self.order_ticket.split_order([OrderBookColumns.order_id.value, order_id])
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_second_lvl_fields_list(
            {OrderBookColumns.qty.value: self.qty_to_split})
        # endregion
        # region heck field
        self.order_ticket.set_order_details(display_qty=self.qty_to_display)
        self.order_ticket.split_order([OrderBookColumns.order_id.value, order_id])
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_second_lvl_fields_list(
            {OrderBookColumns.display_qty.value: self.qty_to_display})
        # endregion
