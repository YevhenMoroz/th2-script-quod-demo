import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import try_except
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from win_gui_modules.utils import set_session_id

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_1014(TestCase):
    def __init__(self, report_id, session_id, dataset):
        super().__init__(report_id, session_id, dataset)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)

    # @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        order_book = OMSOrderBook(self.case_id, self.session_id)
        order_ticket = OMSOrderTicket(self.case_id, self.session_id)
        base_window = BaseMainWindow(self.case_id, self.session_id)
        client = self.data_set.get_client_by_name('client_pt_1')
        price = '100'
        qty = '50'
        desk = 'Desk of Order Book'
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        user = Stubs.custom_config['qf_trading_fe_user']
        # endregion

        # region open FE
        # endregion
        session_id2 = set_session_id()
        base_window2 = BaseMainWindow(case_id=self.case_id, session_id=session_id2)
        # region create CO order
        order_ticket.set_order_details(client=client, limit=price, qty=qty, tif='Day', recipient=user,
                                       partial_desk=True)
        order_ticket.create_order(lookup='VETO')
        # order_book.scroll_order_book(1)
        order_id_first = order_book.extract_field('Order ID')
        # endregion

        # region switch user

        base_window2.open_fe(self.report_id, folder=work_dir, user='ishevchenko', password='ishevchenko', is_open=False)
        base_window2.switch_user()
        print('Wow')
        # endregion

        # region accept CO order
        order_inbox = OMSClientInbox(self.case_id, session_id2)
        order_inbox.accept_order('O', 'M', 'S')
        # endregion

        # region verify values
        order_book_2 = OMSOrderBook(self.case_id, session_id=session_id2)
        status = order_book_2.extract_field('Sts')
        order_id = order_book_2.extract_field('Order ID')
        base_window2.compare_values({'Sts': 'Open', 'Order ID': order_id_first}, {'Sts': status, 'Order ID': order_id},
                                    "Event_Name")
        # endregion

    try_except(test_id=os.path.basename(__file__))

    def run_post_conditions(self):
       pass
