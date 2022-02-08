import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.DataSet import Connectivity
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
class QAP_1406(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = Connectivity.Ganymede_317_ss.value
        self.fix_manager = FixManager(self.ss_connectivity)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_market()
        self.fix_message.change_parameter("Account", "client2341")
        self.lookup = "VETO"
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.client = data_set.get_client_by_name("client_co_1")
        self.route = data_set.get_route("route_1")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region group modify
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).group_modify(client=self.client, security_account= "CLIENT_FIX_CARE_SA1", routes=self.route)
        # endregion
        # region accept order
        self.client_inbox.accept_order(self.lookup, self.qty, "10")
        # endregion
        # region check open status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion

