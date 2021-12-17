import logging
import os
import time
from rule_management import RuleManager
from test_framework.win_gui_wrappers.base_window import decorator_try_except

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_480(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_480(self):
        # region Declaration
        order_book = OMSOrderBook(self.case_id, self.session_id)
        order_ticket = OMSOrderTicket(self.case_id, self.session_id)
        base_window = BaseMainWindow(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        route = 'Route via FIXBUYTH2 - component'
        fix_manager = FixManager(self.ss_connectivity)
        fix_message = FixMessageNewOrderSingleOMS().set_default_care_limit()

        # endregion

        # region open FE
        base_window.open_fe(self.report_id, work_dir, username, password, True)
        # endregion
        # region create CO order
        fix_manager.send_message_fix_standard(fix_message)
        # endregion

        # region accept CO order
        order_inbox = OMSClientInbox(self.case_id, self.session_id)
        order_inbox.accept_order('O', 'M', 'S')
        # endregion

        order_book.set_error_message_details()
        result = order_book.direct_loc_extract_error_message('0', route)
        order_book.compare_values({'ErrorMessage': 'Error - Qty Percentage should be greater than zero (0)'}, result,
                                  'Verify Error message')

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_480()
