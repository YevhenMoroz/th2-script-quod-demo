import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.DataSet import Connectivity
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, OrderType
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_1068(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = Connectivity.Ganymede_317_ss.value
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_market()
        self.route = self.data_set.get_route("route_1")
        self.qty_percentage = "100"
        self.price = "20"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # endregion
        # region create CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        lookup = self.fix_message.get_parameter('Instrument')
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        self.client_inbox.accept_order('O', 'M', 'S')
        # endregion
        # region check market order has open status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.ord_type.value: OrderType.market.value,OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion
        self.order_book.direct_moc_order_correct(self.qty_percentage, self.route)
        # endregion
        # region check open child status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_second_lvl_fields_list(
            {OrderBookColumns.qty.value: qty, OrderBookColumns.sts.value: ExecSts.sent.value})
        # endregion



