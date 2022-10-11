import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.core.test_case import TestCase
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7411(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.qty = "1000"
        self.price = "50"
        self.fix_message.change_parameters({'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price})
        self.lookup = self.data_set.get_lookup_by_name('lookup_2')
        self.route = self.data_set.get_route("route_2")
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.qty_type = self.data_set.get_qty_type('qty_type_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        # endregion
        # region accept CO order
        self.client_inbox.accept_order()
        # endregion
        # region do direct child care and extract error
        result = self.order_book.direct_child_care_order(extracted_error=True, qty_percentage="0",
                                                         qty_type=self.qty_type, route=self.route)
        print(result)
        self.order_book.compare_values({"": 'Error - Qty Percentage should be greater than zero (0)'},
                                       result, "Check error in footer of DirectChildCare Ticket")
        # endregion
