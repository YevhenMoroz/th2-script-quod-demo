import logging
from datetime import datetime

from th2_grpc_hand import rhbatch_pb2
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.eq_wrappers import switch_user
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from win_gui_modules.utils import get_base_request, prepare_fe, get_opened_fe, close_fe
from win_gui_modules.wrappers import set_base

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
qty2 = "100"
price = "20"
price2 = "1"
order_type = "Limit"


class QAP_1022(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

    def run_pre_conditions_and_steps(self):
        case_name = "QAP-1022"
        seconds, nanos = timestamps()  # Store case start time

        # region Declarations
        act = Stubs.win_act_order_book
        client = self.data_set.get_client_by_name('client_co_1')
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        # endregion
        # region Open FE
        stub = Stubs.win_act
        # case_id = create_event(case_name, report_id)
        session_id2 = Stubs.win_act.register(
            rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
        base_window = BaseMainWindow(self.test_id, self.session_id)
        base_window2 = BaseMainWindow(self.test_id, session_id2)
        order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        order_book = OMSOrderBook(self.test_id, self.session_id)
        client_inbox = OMSClientInbox(self.test_id, self.session_id)

        # endregion
        # region Switch to user1
        base_window.open_fe(self.report_id, work_dir, username, password, True)
        base_window2.open_fe(self.report_id, work_dir, username2, password2, False)
        # endregion
        # region Create CO
        order_ticket.set_order_details(client=client, limit=price, qty=qty, order_type=order_type,
                                       tif='Day', is_sell_side=False, instrument=lookup, recipient=desk, partial_desk=False)
        order_ticket.create_order(lookup=lookup)
        order_id = order_book.extract_field('Order ID')
        # endregion
        # region Check values in OrderBook
        order_book.set_filter(['Order ID', order_id]).check_order_fields_list(
            {"Sts": "Sent"})
        # endregion
        # region Accept CO
        client_inbox.accept_order(lookup, qty, price)
        # endregion
        # region Check values in OrderBook after Accept
        order_book.set_filter(['Order ID', order_id]).check_order_fields_list(
            {"Sts": "Open"})
        # endregion
        # region Switch to user2


        # endregion
        # region Amend order
        base_window2.switch_user()
        order_ticket.set_order_details(limit=price2, qty=qty2)
        order_ticket.amend_order(['Order ID', order_id])
        client_inbox.accept_order(lookup, qty2, price2)
        order_book.check_order_fields_list(
            {"Qty": qty2, "Limit": price2})
        # endregion

        # region Cancelling order
        base_window.switch_user()
        order_book.cancel_order()
        # endregion

        # region Check values after Cancel
        base_window2.switch_user()
        client_inbox.accept_and_cancel_children(lookup, qty2, price2)
        order_book.set_filter(['Order ID', order_id]).check_order_fields_list(
            {"Sts": "Cancelled"})
        # endregion

        logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
