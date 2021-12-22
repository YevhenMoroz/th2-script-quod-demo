import logging
import os
import time

from custom import basic_custom_actions as bca
from rule_management import RuleManager
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
from test_framework.win_gui_wrappers.base_window import decorator_try_except

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_3503(TestCase):
    def __init__(self, report_id, session_id):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__)[:-3], self.test_id)
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity
        self.dc_connectivity = SessionAliasOMS().dc_connectivity

    def qap_3503(self):
        # region Declaration
        fix_manager = FixManager(self.ss_connectivity, self.report_id)
        fix_verifier = FixVerifier(self.ss_connectivity, self.case_id)
        fix_verifier_dc = FixVerifier(self.dc_connectivity, self.case_id)
        client = "CLIENT_COUNTERPART2"
        account = "CLIENT_COUNTERPART2_SA1"
        # endregion
        # region DMA order
        change_params = {'Account': client,
                         'PreAllocGrp': {
                             'NoAllocs': [{
                                 'AllocAccount': account,
                                 'AllocQty': "100"}]}, }
        nos = FixMessageNewOrderSingleOMS().set_default_dma_limit(Instrument.FR0004186856).change_parameters(change_params)
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
        # region Set-up parameters for ExecutionReports
        parties = {
            'NoPartyIDs': [
                {'PartyRole': "5",
                 'PartyID': "InvestorID - ClCounterpart2_SA1",
                 'PartyIDSource': "C"},
                {'PartyRole': "22",
                 'PartyID': "Exchange - ClCountepart2",
                 'PartyIDSource': "C"},
                {'PartyRole': "28",
                 'PartyID': "CustodianUser",
                 'PartyIDSource': "C"},
                {'PartyRole': "34",
                 'PartyID': "RegulatoryBody - Venue(Paris)",
                 'PartyIDSource': "C"},
                {'PartyRole': "66",
                 'PartyID': "MarketMaker - TH2Route",
                 'PartyIDSource': "C"},
                {'PartyRole': "10",
                 'PartyID': "CREST",
                 'PartyIDSource': "D"}
            ]
        }
        exec_report1 = FixMessageExecutionReportOMS().set_default_new(nos).change_parameters({"Parties": parties})
        exec_report2 = FixMessageExecutionReportOMS().set_default_filled(nos).change_parameters({"Parties": parties})
        # endregion
        # region Check ExecutionReports
        fix_verifier.check_fix_message_fix_standard(exec_report1)
        fix_verifier.check_fix_message_fix_standard(exec_report2)
        # endregion
        # region Set-up parameters Confirmation report
        no_party = {
            'NoParty': parties['NoPartyIDs']
        }
        conf_report = FixMessageConfirmationReportOMS().set_default_confirmation_new(nos).change_parameters(
            {"NoParty": no_party})
        alloc_report = FixMessageAllocationInstructionReportOMS().set_default_preliminary(nos)
        # endregion
        # region Check Book & Allocation
        fix_verifier_dc.check_fix_message_fix_standard(conf_report)
        fix_verifier_dc.check_fix_message_fix_standard(alloc_report)
        # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_3503()
