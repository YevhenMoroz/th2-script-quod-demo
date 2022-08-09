import logging
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.DataSet import Connectivity
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.core.test_case import TestCase
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, OrderType, TimeInForce
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7624(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.lookup = "DNX"
        self.route = self.data_set.get_route("route_1")
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.qty = "900"
        self.price = "20"
        self.order_type = "Limit"
        self.client = self.data_set.get_client_by_name('client_co_1')
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.desk = environment.get_list_fe_environment()[0].desk_3
        self.route = self.data_set.get_route("route_1")
        self.qty_type = self.data_set.get_qty_type('qty_type_1')


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        self.order_ticket.set_order_details(client=self.client, limit=self.price, qty=self.qty,
                                            order_type=self.order_type,
                                            tif=TimeInForce.DAY.value, is_sell_side=False, instrument=self.lookup,
                                            recipient=self.desk)
        self.order_ticket.create_order(lookup=self.lookup)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region accept CO order
        self.client_inbox.accept_order()
        # endregion
        # region check order open status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.open.value})
        # region DirectLOC CO order
        self.order_book.direct_loc_order(self.qty, self.route, self.qty_type)
        # endregion
        # region check child order has open status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_second_lvl_fields_list(
            {OrderBookColumns.ord_type.value: OrderType.limit.value, OrderBookColumns.qty.value: self.qty, OrderBookColumns.tif.value: TimeInForce.ATC.value})
        # endregion
