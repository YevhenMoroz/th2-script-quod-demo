import logging
from th2_grpc_hand import rhbatch_pb2
from custom.basic_custom_actions import create_event
from stubs import Stubs
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.fe_trading_constant import TimeInForce, OrderBookColumns,  OrderType
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from win_gui_modules.utils import close_fe, set_session_id

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True



@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7677(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fe_env = self.environment.get_list_fe_environment()[0]
        self.username2 = self.fe_env.user_2
        self.qty = "900"
        self.price = "20"
        self.qty_to_split = "400"
        self.qty_to_display = "400"
        self.order_type = OrderType.limit.value
        self.client = self.data_set.get_client_by_name('client_co_1')
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.session_id2 = set_session_id(self.fe_env.target_server_win)
        self.base_window = BaseMainWindow(self.test_id, self.session_id)
        self.base_window2 = BaseMainWindow(self.test_id, self.session_id2)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.order_ticket2 = OMSOrderTicket(self.test_id, self.session_id2)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.order_book_2 = OMSOrderBook(self.test_id, self.session_id2)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_book2 = OMSOrderBook(self.test_id, self.session_id2)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declarations
        # region Open FE
        self.base_window2.open_fe(self.report_id, self.fe_env, 2, False)
        # endregion
        # region switch user 1
        self.base_window.switch_user()
        # endregion
        # region Create CO
        self.order_ticket.set_order_details(client=self.client, limit=self.price, qty=self.qty, order_type=self.order_type,
                                       tif=TimeInForce.DAY.value, is_sell_side=False, instrument=self.lookup, recipient=self.username2)
        self.order_ticket.create_order(lookup=self.lookup)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region Accept
        self.client_inbox.accept_order()
        # endregion
        # region switch user 2
        self.base_window2.switch_user()
        # endregion
        # region Split
        self.order_ticket2.set_order_details(qty=self.qty_to_split)
        self.order_ticket2.split_order([OrderBookColumns.order_id.value, order_id])
        self.order_book2.set_filter([OrderBookColumns.order_id.value, order_id]).check_second_lvl_fields_list(
            {OrderBookColumns.qty.value: self.qty_to_split})
        # endregion
        # region Verify
        self.order_ticket2.set_order_details(display_qty=self.qty_to_display)
        self.order_ticket2.split_order([OrderBookColumns.order_id.value, order_id])
        self.order_book2.set_filter([OrderBookColumns.order_id.value, order_id]).check_second_lvl_fields_list(
            {OrderBookColumns.qty.value: self.qty_to_display})
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        close_fe(self.test_id, self.session_id2)
