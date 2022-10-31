import logging
from th2_grpc_hand import rhbatch_pb2
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.fe_trading_constant import TimeInForce, OrderBookColumns, ExecSts, OrderType
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from win_gui_modules.utils import close_fe, set_session_id

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7680(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fe_env = self.environment.get_list_fe_environment()[0]
        self.desk = self.fe_env.desk_1
        self.qty = "900"
        self.qty2 = "1000"
        self.price = "20"
        self.price2 = "10"
        self.order_type = OrderType.limit.value
        self.client = self.data_set.get_client_by_name('client_co_1')
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.session_id2 = set_session_id(self.fe_env.target_server_win)
        self.base_window = BaseMainWindow(self.test_id, self.session_id)
        self.base_window2 = BaseMainWindow(self.test_id, self.session_id2)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.order_book2 = OMSOrderBook(self.test_id, self.session_id2)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_ticket2 = OMSOrderTicket(self.test_id, self.session_id2)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declarations
        # region Open FE
        self.base_window2.open_fe(self.report_id, self.fe_env, 2, False)
        # endregion
        # region Create CO
        self.base_window.switch_user()
        self.order_ticket.set_order_details(client=self.client, limit=self.price, qty=self.qty, order_type=self.order_type,
                                       tif=TimeInForce.DAY.value, is_sell_side=False, instrument=self.lookup, recipient=self.desk, partial_desk=False)
        self.order_ticket.create_order(lookup=self.lookup)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region Accept CO
        self.client_inbox.accept_order()
        # endregion
        # region Check values in OrderBook after Accept
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion
        # region Switch to user2
        # endregion
        # region Amend order
        self.base_window2.switch_user()
        self.order_ticket2.set_order_details(limit=self.price2, qty=self.qty2)
        self.order_ticket2.amend_order([OrderBookColumns.order_id.value, order_id])
        self.base_window.switch_user()
        self.client_inbox.accept_modify_plus_child()
        self.order_book.check_order_fields_list(
            {OrderBookColumns.qty.value: self.qty2, OrderBookColumns.limit_price.value: self.price2})
        # endregion
        # region Cancelling order
        self.base_window2.switch_user()
        self.order_book2.cancel_order(False, 1, filter_list=[OrderBookColumns.order_id.value, order_id])
        # endregion
        # region Check values after Cancel
        self.base_window.switch_user()
        self.client_inbox.accept_and_cancel_children()
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.cancelled.value})
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        close_fe(self.test_id, self.session_id2)
