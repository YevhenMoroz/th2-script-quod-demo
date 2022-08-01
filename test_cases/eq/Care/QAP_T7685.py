import logging
from test_framework.core.test_case import TestCase
from custom import basic_custom_actions as bca
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import TimeInForce, OrderBookColumns, ExecSts, OrderType
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from stubs import Stubs
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7685(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.username = environment.get_list_fe_environment()[0].user_1
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.client = self.data_set.get_client_by_name('client_co_1')
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.order_type = OrderType.limit.value
        self.qty = "900"
        self.price = "20"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declarations
        # endregion
        # region Create CO
        self.order_ticket.set_order_details(client=self.client, limit=self.price, qty=self.qty,
                                            order_type=self.order_type, tif=TimeInForce.DAY.value, is_sell_side=False,
                                            instrument=self.lookup, recipient=self.username, partial_desk=True)
        self.order_ticket.create_order(lookup=self.lookup)
        # endregion
        # region Check values in OrderBook
        self.order_book.check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.open.value, OrderBookColumns.qty.value: self.qty,
             OrderBookColumns.client_name.value: self.client, OrderBookColumns.limit_price.value: self.price})
        # endregion
