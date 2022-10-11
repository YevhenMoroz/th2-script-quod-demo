import logging
import os
import time
from pathlib import Path

from th2_grpc_hand import rhbatch_pb2

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from win_gui_modules.utils import set_session_id, close_fe

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

ss_connectivity = SessionAliasOMS().ss_connectivity
bs_connectivity = SessionAliasOMS().bs_connectivity


class QAP_T7248(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.recipient = Stubs.custom_config['qf_trading_fe_user']
        self.work_dir = Stubs.custom_config['qf_trading_fe_folder']
        self.recipient_2 = Stubs.custom_config['qf_trading_fe_user_2']
        self.qty = '100'
        self.price = '100'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region switch on second user
        session_id2 = Stubs.win_act.register(
            rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
        base_window_2 = BaseMainWindow(case_id=self.test_id, session_id=session_id2)
        order_book_2 = OMSOrderBook(self.test_id, session_id2)
        base_window_2.open_fe(self.report_id, folder=self.work_dir, user=self.recipient_2, password=self.recipient_2,
                              is_open=False)
        # endregion
        # region switch on 1 user again
        base_window = BaseMainWindow(case_id=self.test_id, session_id=self.session_id)
        base_window.switch_user()
        # endregion

        # region creating order
        self.order_ticket.set_order_details(self.data_set.get_client_by_name('client_pt_1'), limit=self.price,
                                            qty=self.qty,
                                            recipient=self.recipient, partial_desk=True)
        self.order_ticket.create_order(self.data_set.get_lookup_by_name('lookup_1'))

        # endregion

        # region verifying of Status
        order_sts = self.order_book.extract_field(OrderBookColumns.sts.value)
        self.order_book.compare_values({OrderBookColumns.sts.value: 'Open'},
                                       {OrderBookColumns.sts.value: order_sts}, 'Comparing values')

        # endregion

        # region transfer on second user
        self.order_book.transfer_order(desk=self.recipient_2, partial_desk=False)
        base_window_2.switch_user()
        # endregion

        # region accept in Internal Transfer
        order_book_2.internal_transfer(True)
        close_fe(self.test_id, session_id2)
        base_window.switch_user()
        # endregion

        # region manual execute CO order form first user
        self.order_book.manual_execution(qty=self.qty, price=self.price)
        # endregion

        # region extraction values
        order_sts = self.order_book.extract_fields_list(
            {OrderBookColumns.exec_sts.value: OrderBookColumns.exec_sts.value,
             OrderBookColumns.exec_progress.value:
                 OrderBookColumns.exec_progress.value,
             OrderBookColumns.owner.value: OrderBookColumns.owner.value})

        self.order_book.compare_values({OrderBookColumns.exec_sts.value: 'Filled',
                                        OrderBookColumns.exec_progress.value: '100%',
                                        OrderBookColumns.owner.value: self.recipient}, order_sts, 'Comparing values')
        # endregion
