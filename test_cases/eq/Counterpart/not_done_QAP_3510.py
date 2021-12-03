import logging
import os
import time

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_framework.fix_wrappers.DataSet import Instrument
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOfficeBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP3510(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_3510(self):
        # region Declaration
        fix_manager = FixManager(self.ss_connectivity, self.report_id)
        fix_verifier = FixVerifier(self.ss_connectivity, self.case_id)
        main_window = BaseMainWindow(self.case_id, self.session_id)
        middle_office = OMSMiddleOfficeBook(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        client = "CLIENT_COUNTERPART"
        # endregion
        # region Open FE
        # main_window.open_fe(self.report_id, work_dir, username, password)
        # endregion
        # region DMA order
        change_params = {'Account': client,
                         'ExDestination': 'XEUR',
                         'PreAllocGrp': {
                             'NoAllocs': [{
                                 'AllocAccount': "CLIENT_COUNTERPART_SA1",
                                 'AllocQty': "100"}]}, }
        nos = FixMessageNewOrderSingleOMS().set_default_dma_limit(Instrument.ISI1).change_parameters(change_params)
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                             client + "_EUREX", "XEUR",
                                                                                             20)
            trade_rele = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                       client + "_EUREX", "XEUR", 20,
                                                                                       100, 2)

            fix_manager.send_message_and_receive_response_fix_standard(nos)
        finally:
            time.sleep(1)
            rule_manager.remove_rule(nos_rule)
            rule_manager.remove_rule(trade_rele)
        # endregion
        # region Set-up parameters for ExecutionReports
        exec_report1 = FixMessageExecutionReportOMS().set_default_new(nos)
        exec_report2 = FixMessageExecutionReportOMS().set_default_filled(nos)
        # endregion
        # region Check ExecutionReports
        fix_verifier.check_fix_message_fix_standard(exec_report1)
        fix_verifier.check_fix_message_fix_standard(exec_report2)
        # endregion
        # # region Book order
        # middle_office.book_order()
        # # endregion
        # # region Allocate order
        # middle_office.approve_block()
        # middle_office.allocate_block()
        # # endregion
        # region Set-up parameters for Allocation & Confirmation reports
        book_report = FixMessageAllocationInstructionReportOMS().set_default_ready_to_book(nos)
        alloc_report = FixMessageAllocationInstructionReportOMS().set_default_preliminary(nos)
        conf_report = FixMessageConfirmationReportOMS().set_default_confirmation_new(nos)
        # endregion
        # region Check Book & Allocation
        #fix_verifier.check_fix_message_fix_standard(book_report)
        #fix_verifier.check_fix_message_fix_standard(alloc_report)
        fix_verifier.check_fix_message_fix_standard(conf_report)
        # endregion

    # @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_3510()
