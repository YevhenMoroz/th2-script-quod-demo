import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from th2_grpc_hand import rhbatch_pb2
from stubs import Stubs
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.fe_trading_constant import TimeInForce, OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from win_gui_modules.utils import close_fe

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_1017(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.client = self.data_set.get_client_by_name('client_co_1')
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.work_dir = Stubs.custom_config['qf_trading_fe_folder']
        self.username = Stubs.custom_config['qf_trading_fe_user']
        self.password = Stubs.custom_config['qf_trading_fe_password']
        self.username2 = Stubs.custom_config['qf_trading_fe_user_2']
        self.password2 = Stubs.custom_config['qf_trading_fe_password_2']
        self.qty = "900"
        self.price = "20"
        self.order_type = "Limit"
        self.session_id2 = Stubs.win_act.register(
            rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
        self.base_window2 = BaseMainWindow(self.test_id, self.session_id2)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):

        # region Declarations
        # endregion
        # region Open FE
        self.base_window2.open_fe(self.report_id, self.work_dir, self.username2, self.password2, False)
        # endregion
        # region Create CO
        self.order_ticket.set_order_details(client=self.client, limit=self.price, qty=self.qty, order_type=self.order_type,
                                       tif=TimeInForce.DAY.value, is_sell_side=False, instrument=self.lookup, recipient=self.username2)
        self.order_ticket.create_order(lookup=self.lookup)
        # endregion
        # region Check values in OrderBook
        self.order_book.set_filter([OrderBookColumns.order_id.value, self.order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: "Sent"})
        # endregion
        # region switch to user2
        self.base_window2.switch_user()
        # endregion
        # region Accept CO
        self.client_inbox.accept_order(self.lookup, self.qty, self.price)
        # endregion
        # region Check values in OrderBook after Accept
        self.order_book.set_filter([OrderBookColumns.order_id.value, self.order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion


    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        close_fe(self.test_id, self.session_id2)

