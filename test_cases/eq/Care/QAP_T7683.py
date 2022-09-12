import logging
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import create_event
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.fe_trading_constant import TimeInForce, OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from win_gui_modules.utils import close_fe, set_session_id
from test_framework.core.test_case import TestCase

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7683(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment= None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fe_env = self.environment.get_list_fe_environment()[0]
        self.username2 = self.fe_env.user_2
        self.qty = "900"
        self.price = "20"
        self.order_type = "Limit"
        self.client = self.data_set.get_client_by_name('client_co_1')
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.session_id2 = set_session_id(self.fe_env.target_server_win)
        self.init_event = create_event("Initialization", parent_id=self.report_id)
        self.base_window = BaseMainWindow(self.test_id, self.session_id)
        self.base_window2 = BaseMainWindow(self.test_id, self.session_id2)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.order_book_2 = OMSOrderBook(self.test_id, self.session_id2)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id2)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declarations
        # region Open FE
        self.base_window2.open_fe(self.report_id, self.fe_env, 2, False)
        # endregion
        # region Create CO
        self.base_window.switch_user()
        self.order_ticket.set_order_details(client=self.client, limit=self.price, qty=self.qty, order_type=self.order_type,
                                       tif=TimeInForce.DAY.value, is_sell_side=False, instrument=self.lookup, recipient=self.username2)
        self.order_ticket.create_order(lookup=self.lookup)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region Check values in OrderBook
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.sent.value})
        # endregion
        # region switch to user2
        self.base_window2.switch_user()
        # endregion
        # region Accept CO
        self.client_inbox.reject_order()
        # endregion
        # region Check values in OrderBook after Accept
        self.order_book_2.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.rejected.value})
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        close_fe(self.test_id, self.session_id2)

