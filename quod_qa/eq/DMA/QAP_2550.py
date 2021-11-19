import logging
import os

from custom.basic_custom_actions import create_event
from custom import basic_custom_actions as bca
from quod_qa.win_gui_wrappers.TestCase import TestCase
from quod_qa.win_gui_wrappers.base_window import BaseWindow, decorator_try_except
from quod_qa.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from quod_qa.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from quod_qa.wrapper_test.SessionAlias import SessionAliasOMS
from rule_management import RuleManager
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

# Need Import layout
"""
FYI ,MASTER, IVAN,EUGEN, VADIM!!!!
"""


class QAP2550(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_2550(self):
        # region Declarations
        qty = "900"
        price = "30"
        client = "CLIENT_COMM1"
        account = 'CLIENT_COMM_1_SA1'
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        base_window = BaseWindow(self.case_id, self.session_id)
        oms_order_ticket = OMSOrderTicket(self.case_id, self.session_id)
        oms_order_book = OMSOrderBook(self.case_id, self.session_id)
        rule_manager = RuleManager()
        base_window.open_fe(self.report_id, work_dir, username, password)
        # endregion
        try:
            nos_rule = RuleManager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.ss_connectivity,
                                                                                            client + '_PARIS'
                                                                                            , 'XPAR', float(price))
            oms_order_ticket.set_order_details(client=client, limit=price, qty=qty, tif='Day',
                                               account=account, washbook='CareWB')
            oms_order_ticket.oms_create_order()
        except Exception:
            logger.error('THIS IS ERROR, MAN')
        finally:
            rule_manager.remove_rule(nos_rule)
        order_id = oms_order_book.extract_field('Order ID')
        oms_order_book.set_filter(["Order ID", order_id])
        oms_order_book.check_order_fields_list({'Account ID': account, 'Wash Book': 'CareWB'}, 'Check in Order Book', 1)

    # @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_2550()
