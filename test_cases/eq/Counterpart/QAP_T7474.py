import logging
import time
from copy import deepcopy

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7474(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.client = self.data_set.get_client_by_name("client_counterpart_1")
        self.client_acc = self.data_set.get_account_by_name("client_counterpart_1_acc_1")
        self.change_params = {'Account': self.client,
                              'PreAllocGrp': {
                                  'NoAllocs': [{
                                      'AllocAccount': self.client_acc,
                                      'AllocQty': "200"}]}}
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.qty = "200"
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.price = self.fix_message.get_parameter("Price")
        self.fix_message.change_parameters(self.change_params)
        self.rule_manager = RuleManager(Simulators.equity)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_counterpart_1_venue_1")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        nos_rule = None
        trade_rule = None
        try:

            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.mic, int(self.price),
                                                                                            int(self.qty), 2)

            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion
        # region Set-up parameters for ExecutionReports
        list_of_ignored_fields = ['NoMiscFees', 'Account', 'CommissionData', 'MiscFeesGrp', 'ReplyReceivedTime',
                                  'SecurityDesc', 'OrderAvgPx', 'GatingRuleCondName', 'GatingRuleName',
                                  'PartyRoleQualifier', 'tag11245', 'PartyRoleQualifier']
        list_of_counterparts = [
            self.data_set.get_counterpart_id_fix('counterpart_id_investment_firm_cl_counterpart_sa1'),
            self.data_set.get_counterpart_id_fix('counterpart_id_regulatory_body_venue_paris'),
            self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user_2'),
            self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
            self.data_set.get_counterpart_id_fix('counterpart_id_investment_firm_cl_counterpart'),
            {'PartyRole': '*',
             'PartyRoleQualifier': '*',
             'PartyID': '*',
             'PartyIDSource': '*'}
        ]
        parties = {
            'NoPartyIDs': list_of_counterparts
        }
        exec_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_new(self.fix_message).change_parameters(
            {"Parties": parties, "ReplyReceivedTime": "*", "SecondaryOrderID": "*", "LastMkt": "*", "Text": "*"})
        exec_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_filled(
            self.fix_message).change_parameters(
            {"Parties": parties, "ReplyReceivedTime": "*", "SecondaryOrderID": "*", "LastMkt": "*", "Text": "*",
             "Account": self.client_acc})
        exec_report2.remove_parameter("SettlCurrency")
        # endregion
        # region Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(exec_report1, ignored_fields=list_of_ignored_fields)
        self.fix_verifier.check_fix_message_fix_standard(exec_report2, ignored_fields=list_of_ignored_fields)
        # endregion
        # region Set-up parameters Confirmation report
        list_of_counterparts_allocation = [
            self.data_set.get_counterpart_id_fix('counterpart_id_investment_firm_cl_counterpart_sa1'),
            self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user_2'),
            self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
            self.data_set.get_counterpart_id_fix('counterpart_id_investment_firm_cl_counterpart'),
            {'PartyRole': '*',
             'NoPartySubIDs': '*',
             'PartyID': '*',
             'PartyIDSource': '*'},
            {'PartyRole': '*',
             'PartyID': '*',
             'PartyIDSource': '*'},
        ]
        list_of_counterparts_confirmation = [
            self.data_set.get_counterpart_id_fix('counterpart_id_investment_firm_cl_counterpart_sa1'),
            self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user_2'),
            self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
            self.data_set.get_counterpart_id_fix('counterpart_id_investment_firm_cl_counterpart'),
            {'PartyRole': '*',
             'NoPartySubIDs': '*',
             'PartyID': '*',
             'PartyIDSource': '*'},
        ]
        no_party1 = {
            'NoParty': list_of_counterparts_confirmation
        }
        no_party2 = {
            'NoParty': list_of_counterparts_allocation
        }
        conf_report = FixMessageConfirmationReportOMS(self.data_set).set_default_confirmation_new(
            self.fix_message).change_parameters(
            {"NoParty": no_party1, "Account": self.client, "tag5120": "*"})
        alloc_report = FixMessageAllocationInstructionReportOMS().set_default_preliminary(
            self.fix_message).change_parameters(
            {"NoParty": no_party2, "Account": self.client, "tag5120": "*"})
        alloc_report.change_parameter('NoAllocs', "*")
        # endregion
        # region Check Book & Allocation
        self.fix_verifier_dc.check_fix_message_fix_standard(conf_report, ignored_fields=list_of_ignored_fields)
        self.fix_verifier_dc.check_fix_message_fix_standard(alloc_report, ignored_fields=list_of_ignored_fields)
        # endregion
