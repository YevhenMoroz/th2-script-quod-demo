import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from th2_grpc_hand import rhbatch_pb2
from custom.basic_custom_actions import create_event, timestamps
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
work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']
username2 = Stubs.custom_config['qf_trading_fe_user_2']
password2 = Stubs.custom_config['qf_trading_fe_password_2']
qty = "900"
price = "20"
order_type = "Limit"


class QAP_1017(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        seconds, nanos = timestamps()  # Store case start time
        client = self.data_set.get_client_by_name('client_co_1')
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        # region Declarations
        # endregion
        # region Open FE
        session_id2 = Stubs.win_act.register(
            rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
        base_window2 = BaseMainWindow(self.test_id, session_id2)
        order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        order_book = OMSOrderBook(self.test_id, self.session_id)
        client_inbox = OMSClientInbox(self.test_id, self.session_id)
        # endregion
        # region switch to user1
        base_window2.open_fe(self.report_id, work_dir, username2, password2, False)
        # endregion
        # region Create CO
        order_ticket.set_order_details(client=client, limit=price, qty=qty, order_type=order_type,
                                       tif=TimeInForce.DAY.value, is_sell_side=False, instrument=lookup, recipient=username2)
        order_ticket.create_order(lookup=lookup)
        order_id = order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region Check values in OrderBook
        order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: "Sent"})
        # endregion
        # region switch to user2
        # base_window2.open_fe(self.report_id, work_dir, username2, password2, False)
        base_window2.switch_user()
        # endregion
        # region Accept CO
        client_inbox.accept_order(lookup, qty, price)
        # endregion
        # region Check values in OrderBook after Accept
        order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion
        close_fe(self.test_id, session_id2)
