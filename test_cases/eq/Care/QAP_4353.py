import time

from win_gui_modules.utils import get_base_request
import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, Suspended
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_4353(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message2 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message2.change_parameter("Side", '2')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = "5"
        self.base_request = get_base_request(self.session_id, self.test_id)



    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create 1 CO order
        response=self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id1 = response[0].get_parameter("OrderID")
        # endregion
        # region suspend 1 CO order
        self.order_book.suspend_order()
        # endregion
        # region accept 1 CO order
        self.client_inbox.accept_order()
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id1]).check_order_fields_list(
            {OrderBookColumns.suspend.value: Suspended.yes.value})
        # endregion
        # region create 2 CO order
        fix_message_2 = self.fix_message.change_parameter("Side", "2")
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message2)
        order_id2 = response[0].get_parameter("OrderID")
        # endregion
        # region accept 2 CO order
        self.client_inbox.accept_order()
        # endregion
        # region suspend 2 CO order
        time.sleep(5)
        self.order_book.suspend_order()
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id2]).check_order_fields_list(
            {OrderBookColumns.suspend.value: Suspended.yes.value})
        # endregion
        # region manual cross orders
        result = self.order_book.manual_cross_orders([1,2], self.qty, self.price, "XASE", extract_footer=True)
        self.order_book.compare_values({"Trade Ticket Error": "Error - [QUOD-11603] 'ExecPrice' (0) negative or zero"},
                                        result, "Check Error in Manual Cross footer")
        # endregion
