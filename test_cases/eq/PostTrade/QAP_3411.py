import logging
import os
import time

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_framework.ReadLogVerifier import ReadLogVerifier
from test_framework.fix_wrappers.DataSet import Instrument
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import decorator_try_except
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOfficeBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_3411(TestCase):
    def __init__(self, report_id, session_id):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__)[:-3], self.test_id)
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity
        self.als_email_report = SessionAliasOMS().als_email_report

    def QAP_3411(self):
        # region Declaration
        fix_manager = FixManager(self.ss_connectivity, self.case_id)
        read_log_verifier = ReadLogVerifier(self.als_email_report, self.case_id)
        main_win = BaseMainWindow(self.case_id, self.session_id)
        mid_office = OMSMiddleOfficeBook(self.case_id, self.session_id)
        client = "MOClient2"
        account1 = "MOClient2_SA1"
        account2 = "MOClient2_SA2"
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        # endregion
        # region create checkpoint for read-log
        checkpoint_response1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(self.report_id))
        checkpoint = checkpoint_response1.checkpoint
        # endregion
        # region Open FE
        main_win.open_fe(self.report_id, work_dir, username, password)
        # endregion
        # region Create care order

        change_params = {'Account': client,
                         'PreAllocGrp': {'NoAllocs': [{'AllocAccount': account1,
                                                       'AllocQty': "50"},
                                                      {'AllocAccount': account2,
                                                       'AllocQty': "50"}]}}
        nos = FixMessageNewOrderSingleOMS().set_default_dma_limit(Instrument.FR0004186856).change_parameters(
            change_params)
        qty = nos.get_parameters()["OrderQtyData"]["OrderQty"]
        price = nos.get_parameters()["Price"]
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                             client + "_PARIS", "XPAR",
                                                                                             int(price))
            trade_rele = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                       client + "_PARIS", "XPAR",
                                                                                       int(price),
                                                                                       int(qty), 1)

            fix_manager.send_message_and_receive_response_fix_standard(nos)
        finally:
            time.sleep(1)
            rule_manager.remove_rule(nos_rule)
            rule_manager.remove_rule(trade_rele)
        # endregion
        # region Check ALS logs Status New
        als_logs_params = {
            "ConfirmationID": "*",
            "ConfirmStatus": "New",
            "ClientAccountID": account1
        }
        read_log_verifier.check_read_log_message(als_logs_params,["ConfirmStatus"], timeout=30000)
        # endregion
        # region Un-allocate
        mid_office.unallocate_order()
        # endregion
        # region Check ALS logs Status Canceled
        als_logs_params = {
            "ConfirmationID": "*",
            "ConfirmStatus": "Cancel",
            "ClientAccountID": account1
        }
        read_log_verifier.check_read_log_message(als_logs_params, ["ConfirmStatus"], timeout=50000)
        # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.QAP_3411()
