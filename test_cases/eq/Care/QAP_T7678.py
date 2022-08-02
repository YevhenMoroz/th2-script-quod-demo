import logging
from th2_grpc_hand import rhbatch_pb2
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from stubs import Stubs
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, TimeInForce, ExecSts
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from win_gui_modules.utils import  close_fe

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

class QAP_T7678(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.work_dir = Stubs.custom_config['qf_trading_fe_folder']
        self.username = Stubs.custom_config['qf_trading_fe_user']
        self.password = Stubs.custom_config['qf_trading_fe_password']
        self.username2 = Stubs.custom_config['qf_trading_fe_user_2']
        self.password2 = Stubs.custom_config['qf_trading_fe_password_2']
        self.desk = Stubs.custom_config['qf_trading_fe_user_desk']
        self.qty = "900"
        self.price = "40"
        self.order_type = "Limit"
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        self.client = self.data_set.get_client_by_name('client_co_1')
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.base_window = BaseMainWindow(self.test_id, self.session_id)
        self.session_id2 = Stubs.win_act.register(
            rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
        self.base_window2 = BaseMainWindow(self.test_id, self.session_id2)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.order_book2 = OMSOrderBook(self.test_id, self.session_id2)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declarations
        # endregion
        # region open FE
        self.base_window2.open_fe(self.report_id, self.work_dir, self.username2, self.password2, False)
        # endregion
        # region switch user 1
        # endregion
        # region Create CO
        self.base_window.switch_user()
        self.order_ticket.set_order_details(client=self.client, limit=self.price, qty=self.qty, order_type=self.order_type,
                                       tif=TimeInForce.DAY.value, is_sell_side=False, instrument=self.lookup, recipient=self.username2)
        self.order_ticket.create_order(lookup=self.lookup)
        # endregion
        self.order_book.set_filter([OrderBookColumns.order_id.value, self.order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: "Sent"})
        # region switch user 2
        # endregion
        # region Reassign order
        self.base_window2.switch_user()
        self.order_book2.reassign_order(self.username)
        self.order_book2.set_filter([OrderBookColumns.order_id.value, self.order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: "Sent"})
        # endregion
        # region switch user 1
        self.base_window.switch_user()
        # endregion
        # region Accept order
        self.client_inbox.accept_order(self.lookup, self.qty, self.price)
        self.order_book.set_filter([OrderBookColumns.order_id.value, self.order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        close_fe(self.test_id, self.session_id2)


