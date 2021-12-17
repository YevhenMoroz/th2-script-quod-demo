import logging
import os

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_window import BaseWindow, decorator_try_except
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOfficeBook
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP3595(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_3495(self):
        # region Declaration
        base_window = BaseWindow(self.case_id, self.session_id)
        oms_order_book = OMSOrderBook(self.case_id, self.session_id)
        oms_middle_office = OMSMiddleOfficeBook(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        client = 'MOClient4'
        fix_message = FixMessageNewOrderSingleOMS()
        fix_manager = FixManager(self.ss_connectivity, self.case_id)
        fix_message.set_default_care_limit()
        # endregion
        # region open FE
        base_window.open_fe(self.report_id, work_dir, username, password, True)
        # endregion
        # region create DMA order and execute them
        try:
            fix_manager.send_message_fix_standard(fix_message)
            fix_manager.send_message_fix_standard(fix_message)
            fix_manager.send_message_fix_standard(fix_manager)
        except Exception:
            logger.info('Oh shit, I am sorry')
        # endregion
        # endregion
        # region extract orderID from order_book and compare values after autoBook

        order_id = oms_order_book.extract_field('Order ID')
        oms_order_book.complete_order(filter_list=['Order ID', order_id])
        post_trade_status = oms_order_book.extract_field('PostTradeStatus')
        done_for_day = oms_order_book.extract_field('DoneForDay')
        actually_dictionary_of_result = {'PostTradeStatus': post_trade_status, 'DoneForDay': done_for_day}
        oms_order_book.compare_values({'PostTradeStatus': 'Booked', 'DoneForDay': 'Yes'}, actually_dictionary_of_result,
                                      'Compare value after autoBook')

        # endregion
        # region check price after book
        price_of_block = oms_middle_office.extract_block_field('AvgPx', ['Order ID', order_id], 1)
        actually_dictionary_of_result = {'AvgPx': price_of_block}
        print(price_of_block)
        oms_middle_office.compare_values({'AvgPx': '1.124'}, price_of_block, 'Check Price of block')
        # # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_3495()
