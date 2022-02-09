import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from th2_grpc_hand import rhbatch_pb2
from test_framework.core.try_exept_decorator import try_except
from test_framework.old_wrappers.eq_wrappers import *
from stubs import Stubs
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.fe_trading_constant import TimeInForce, OrderBookColumns, ExecSts
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
desk = Stubs.custom_config['qf_trading_fe_user_desk']
qty = "900"
price = "40"
order_type = "Limit"


class QAP_1035(TestCase):

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
        order_book = OMSOrderBook(self.test_id, self.session_id)
        order_book2 = OMSOrderBook(self.test_id, session_id2)
        client_inbox2 = OMSClientInbox(self.test_id, session_id2)
        # endregion
        # region open FE
        base_window2.open_fe(self.report_id, work_dir, username2, password2, False)
        #  endregion
        # region switch to user1
        base_window.switch_user()
        # endregion
        # region create CO
        order_ticket.set_order_details(client=client, limit=price, qty=qty, order_type=order_type,
                                       tif=TimeInForce.DAY.value, is_sell_side=False, instrument=lookup, recipient=username2)
        order_ticket.create_order(lookup=lookup)
        # endregion
        # region Check values in OrderBook
        order_id = order_book.extract_field(OrderBookColumns.order_id.value)
        order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: "Sent"})
        # endregion
        # region switch to user2
        base_window2.switch_user()
        # endregion
        # region accept CO
        client_inbox2.accept_order(lookup, qty, price)
        order_book2.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion
        # region switch to user1
        base_window.switch_user()
        # endregion
        # region manual execution
        order_book.manual_execution()
        # endregion
        # region complete
        order_book.complete_order()
        # endregion
        # region Check values after complete
        order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        # endregion
        close_fe(self.test_id, session_id2)

