import logging
import os
import random
import string
import time

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import decorator_try_except
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOfficeBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP5386(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_5386(self):
        # region Declaration
        fix_manager = FixManager(self.ss_connectivity, self.report_id)
        main_window = BaseMainWindow(self.case_id, self.session_id)
        middle_office = OMSMiddleOfficeBook(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        client = "MOClient"
        # endregion
        # region Open FE
        main_window.open_fe(self.report_id, work_dir, username, password)
        # endregion
        # region DMA order
        nos = FixMessageNewOrderSingleOMS().set_default_dma_limit().change_parameters({'Account': client})
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                             client + "_PARIS", "XPAR",
                                                                                             20)
            trade_rele = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                       client + "_PARIS", "XPAR", 20,
                                                                                       100, 2)

            fix_manager.send_message_and_receive_response_fix_standard(nos)
        finally:
            time.sleep(1)
            rule_manager.remove_rule(nos_rule)
            rule_manager.remove_rule(trade_rele)

        # endregion
        # region Book
        middle_office.set_modify_ticket_details(settl_currency="UAH", exchange_rate="Multiple", exchange_rate_calc="2",
                                                toggle_recompute=True, extract_book=True)
        exp_res = middle_office.book_order()
        middle_office.set_modify_ticket_details(extract_book=True)
        act_res = middle_office.amend_block()
        act_res.pop("book.psetBic")
        # endregion
        # region Verify
        middle_office.compare_values(exp_res, act_res, "compare ticket details")
        # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_5386()
