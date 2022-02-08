import logging
from th2_grpc_hand import rhbatch_pb2
from custom.basic_custom_actions import create_event
from stubs import Stubs
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import BaseWindow
from test_framework.win_gui_wrappers.fe_trading_constant import TimeInForce, OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from win_gui_modules.utils import  close_fe

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']
username2 = Stubs.custom_config['qf_trading_fe_user_2']
password2 = Stubs.custom_config['qf_trading_fe_password_2']
qty = "900"
qty2 = "500"
price = "40"
order_type = "Limit"


class QAP_1026(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declarations
        client = self.data_set.get_client_by_name('client_co_1')
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        # region Declarations
        session_id2 = Stubs.win_act.register(
            rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
        base_window = BaseMainWindow(self.test_id, self.session_id)
        base_window2 = BaseMainWindow(self.test_id, session_id2)
        order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        order_ticket2 = OMSOrderTicket(self.test_id, session_id2)
        order_book = OMSOrderBook(self.test_id, self.session_id)
        order_book2 = OMSOrderBook(self.test_id, session_id2)
        client_inbox = OMSClientInbox(self.test_id, self.session_id)
        client_inbox2 = OMSClientInbox(self.test_id, session_id2)
        # endregion
        # region open FE
        base_window2.open_fe(self.report_id, work_dir, username2, password2, False)
        # endregion
        # region switch user 1
        base_window.switch_user()
        # endregion
        # region Create CO
        order_ticket.set_order_details(client=client, limit=price, qty=qty, order_type=order_type,
                                       tif=TimeInForce.DAY.value, is_sell_side=False, instrument=lookup, recipient=username2)
        order_ticket.create_order(lookup=lookup)
        # endregion
        # region Verify
        order_id = order_book.extract_field(OrderBookColumns.order_id.value)
        order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: "Sent"})
        # endregion
        # region switch user 2
        base_window2.switch_user()
        # endregion
        # region Accept
        client_inbox2.accept_order(lookup, qty, price)
        # endregion
        # region Split
        # endregion
        # region Verify
        order_ticket2.set_order_details(qty=qty2)
        order_ticket2.split_order([OrderBookColumns.order_id.value, order_id])
        order_book2.set_filter([OrderBookColumns.order_id.value, order_id]).check_second_lvl_fields_list(
            {OrderBookColumns.qty.value: qty2})
        # endregion
        close_fe(self.test_id, session_id2)
