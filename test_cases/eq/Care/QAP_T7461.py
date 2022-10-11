import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7461(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.qty = "200"
        self.qty_exec = "100"
        self.price = "10"
        self.price_mc = "8"
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.fix_message.change_parameter("Price", self.price)
        self.last_mkt = "XASE"
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create first CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        # endregion
        # region accept first CO order
        self.client_inbox.accept_order()
        # endregion
        # region create second CO order
        self.fix_message.change_parameter("Side", "2")
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id2 = response[0].get_parameters()['OrderID']
        # endregion
        # region accept second CO order
        self.client_inbox.accept_order()
        # endregion
        # region manual exec order
        self.order_book.manual_execution(qty=self.qty_exec, filter_dict={OrderBookColumns.order_id.value: order_id2})
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id2]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.partially_filled.value})
        # endregion
        # region manual cross orders
        res = self.order_book.manual_cross_orders([1, 2], self.qty, '0', last_mkt=self.last_mkt, extract_footer=True)
        self.order_book.compare_values({"Error": "Error - [QUOD-11603] 'ExecPrice' (0) negative or zero"},
                                       {"Error": res}, "Check Error in Manual Cross footer")
        # endregion
