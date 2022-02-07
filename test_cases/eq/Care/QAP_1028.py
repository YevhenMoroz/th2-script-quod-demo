import logging
from th2_grpc_hand import rhbatch_pb2
from custom.basic_custom_actions import create_event
from stubs import Stubs
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except

from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']
username2 = Stubs.custom_config['qf_trading_fe_user_2']
password2 = Stubs.custom_config['qf_trading_fe_password_2']
desk = Stubs.custom_config['qf_trading_fe_user_desk']
order_type = "Limit"
qty = "900"
price = "40"

class QAP_1028(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declarations
        client = self.data_set.get_client_by_name('client_co_1')
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        order_book = OMSOrderBook(self.test_id, self.session_id)
        client_inbox = OMSClientInbox(self.test_id, self.session_id)
        # endregion
        # region Create CO
        order_ticket.set_order_details(client=client, limit=price, qty=qty, order_type=order_type,
                                       tif='Day', is_sell_side=False, instrument=lookup, recipient=username2)
        order_ticket.create_order(lookup=lookup)
        # endregion
        order_id = order_book.extract_field('Order ID')
        order_book.set_filter(['Order ID', order_id]).check_order_fields_list(
            {"Sts": "Sent"})
        # endregion
        # region Reassign orderQA
        order_book.reassign_order(desk, partial_desk=False)
        # endregion
        # region Reject order
        client_inbox.reject_order(lookup, qty, price)
        # endregion
        order_book.set_filter(['Order ID', order_id]).check_order_fields_list(
            {"Sts": "Rejected"})

