import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import TimeInForce, OrderBookColumns, ExecSts, OrderType
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7679(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.client = self.data_set.get_client_by_name('client_co_1')
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.username2 = environment.get_list_fe_environment()[0].user_2
        self.desk = environment.get_list_fe_environment()[0].desk_1
        self.qty = "900"
        self.price = "40"
        self.order_type = OrderType.limit.value

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create CO
        self.order_ticket.set_order_details(client=self.client, limit=self.price, qty=self.qty,
                                            order_type=self.order_type,
                                            tif=TimeInForce.DAY.value, is_sell_side=False, instrument=self.lookup,
                                            recipient=self.username2)
        self.order_ticket.create_order(self.lookup)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region Reassign order
        self.order_book.reassign_order(self.desk,
                                       partial_desk=False)
        # endregion
        # region Accept order
        self.client_inbox.accept_order()
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion
