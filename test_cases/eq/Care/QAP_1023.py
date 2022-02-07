import logging
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from win_gui_modules.utils import set_session_id, get_base_request

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


# Precondition: add Recpt column
class QAP_1023(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

    def run_pre_conditions_and_steps(self):
        client = self.data_set.get_client_by_name('client_co_1')
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        base_window = BaseMainWindow(self.test_id, self.session_id)
        order_book = OMSOrderBook(self.test_id, self.session_id)
        order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        client_inbox = OMSClientInbox(self.test_id, self.session_id)
        # endregion
        # region open FE
        base_window.open_fe(self.report_id, work_dir, username, password, True)
        # endregion
        # region Create CO
        order_ticket.set_order_details(client=client, limit=price, qty=qty, order_type=order_type,
                                       tif='Day', is_sell_side=False, instrument=lookup, recipient=username2)
        order_ticket.create_order(lookup=lookup)
        order_id = order_book.extract_field('Order ID')
        # endregion
        order_book.set_filter(['Order ID', order_id]).check_order_fields_list(
            {"Sts": "Sent"})
        # region Reassign order
        order_book.reassign_order(desk, partial_desk=False)
        order_book.set_filter(['Order ID', order_id]).check_order_fields_list(
            {"Sts": "Sent"})
        # endregion
        # region Accept order
        client_inbox.accept_order(lookup, qty, price)
        order_book.set_filter(['Order ID', order_id]).check_order_fields_list(
            {"Sts": "Open"})
        # endregion

