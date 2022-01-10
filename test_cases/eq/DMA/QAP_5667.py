import logging
import os
import time
from datetime import datetime
from datetime import timedelta
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

'''
HARD SHIT CODE
'''
class QAP_5667(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__)[:-3], self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity
        self.dc_connectivity = SessionAliasOMS().dc_connectivity
        self.wa_connectivity = SessionAliasOMS().wa_connectivity

    def qap_5667(self):
        # region Declaration
        order_book = OMSOrderBook(self.case_id, self.session_id)
        base_window = BaseMainWindow(self.case_id, self.session_id)
        client_inbox = OMSClientInbox(self.case_id, self.session_id)
        fix_manager = FixManager(self.ss_connectivity, self.case_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        fix_message_new_order_single = FixMessageNewOrderSingleOMS().set_default_dma_limit()
        date = (tm(datetime.utcnow().isoformat()) + bd(n=8)).date()
        date_only = date.strftime('%m/%d/%Y')
        combine_data = date.strftime('%Y-%m-%dT%H:%M:%S')
        fix_message_new_order_single.change_parameter('ExpireTime', combine_data)
        # endregion

        # region open FE
        base_window.open_fe(self.report_id, work_dir, username, password)
        # endregion
        # region create DMA order
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                             'XPAR_' + fix_message_new_order_single.get_parameter(
                                                                                                 'Account'), 'XPAR',
                                                                                             float(
                                                                                                 fix_message_new_order_single.get_parameter(
                                                                                                     'Price')))
            fix_manager.send_message_fix_standard(fix_message_new_order_single)
        except Exception:
            logger.info('Possible error with rule')

        finally:
            time.sleep(3)
            rule_manager.remove_rule(nos_rule)
        # endregion

        expire_time_extract = order_book.extract_field('ExpireTime')
        order_book.compare_values({'ExpireDate': 'True' if expire_time_extract.find(date_only) >= 0 else 'False'},
                                  {'ExpireDate': 'True'},
                                  'Check Expire Data')

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_5667()
