import logging
from datetime import datetime

from th2_grpc_hand import rhbatch_pb2
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from pathlib import Path
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from win_gui_modules.utils import get_base_request, close_fe
from test_framework.core.test_case import TestCase

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


class QAP_1019(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)


    def run_pre_conditions_and_steps(self):
        case_name = "QAP-1019"
        seconds, nanos = timestamps()  # Store case start time

        # region Declarations
        act = Stubs.win_act_order_book

        client = self.data_set.get_client_by_name('client_co_1')
        lookup = self.data_set.get_lookup_by_name('lookup_1')

        # region Declarations
        act = Stubs.win_act_order_book
        # endregion
        # region Open FE
        stub = Stubs.win_act
        case_id = create_event(case_name, self.report_id)
        session_id2 = Stubs.win_act.register(
            rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
        init_event = create_event("Initialization", parent_id=self.report_id)
        base_window = BaseMainWindow(self.test_id, self.session_id)
        base_window2 = BaseMainWindow(self.test_id, session_id2)
        order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        order_book = OMSOrderBook(self.test_id, self.session_id)
        client_inbox = OMSClientInbox(self.test_id, self.session_id)
        # endregion
        # region switch to user1
        base_window.open_fe(self.report_id, work_dir, username, password, True)
        base_window2.open_fe(self.report_id, work_dir, username2, password2, False)
        # endregion
        # region Create CO
        order_ticket.set_order_details(client=client, limit=price, qty=qty, order_type=order_type,
                                       tif='Day', is_sell_side=False, instrument=lookup, recipient=username2)
        order_ticket.create_order(lookup=lookup)
        order_id = order_book.extract_field('Order ID')
        # endregion
        # region Check values in OrderBook
        order_book.set_filter(['Order ID', order_id]).check_order_fields_list(
            {"Sts": "Sent"})
        # endregion
        # region switch to user2
        base_window2.switch_user()
        # endregion
        # region Accept CO
        client_inbox.reject_order(lookup, qty, price)
        # endregion
        # region Check values in OrderBook after Accept
        order_book.set_filter(['Order ID', order_id]).check_order_fields_list(
            {"Sts": "Reject"})
        # endregion

        close_fe(case_id, session_id2)
        logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
