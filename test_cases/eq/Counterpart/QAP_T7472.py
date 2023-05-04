import logging
import time
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
class QAP_T7472(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.client = self.data_set.get_client_by_name("client_counterpart_1")
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.account = self.data_set.get_account_by_name("client_counterpart_1_acc_3")
        self.cur = self.data_set.get_currency_by_name("currency_3")
        self.cur_for_check = self.data_set.get_currency_by_name("currency_2")
        self.change_params = {'Account': self.client,
                              "Currency": self.cur,
                              'ExDestination': self.mic,
                              'PreAllocGrp': {
                                  'NoAllocs': [{
                                      'AllocAccount': self.account,
                                      'AllocQty': "100"}]}}
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit("instrument_3")
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.fix_message.change_parameters(self.change_params)
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_counterpart_1_venue_1")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.mic, float(self.price),
                                                                                            int(self.qty), 2)

            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(trade_rule)
        # endregion
        # region Set-up parameters for ExecutionReports
        party_stub_dict = {'PartyRole': "*",
                           'PartyID': "*",
                           'PartyIDSource': "*"}
        parties = {
            'NoParty': [self.data_set.get_counterpart_id_fix('counterpart_id_investment_firm_cl_counterpart_sa3'),
                        self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user_2'),
                        self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
                        party_stub_dict
                        ]
        }
        ignor_list_new_ord = ['QuodTradeQualifier', 'BookID', 'tag5120', 'ExecBroker', 'Parties', 'SecondaryOrderID',
                              'LastMkt', 'Text', 'GatingRuleCondName', 'GatingRuleName', 'PartyRoleQualifier']
        ignor_list_filled_ord = ['NoMiscFees', 'CommissionData', 'ExecBroker', 'tag5120', 'M_PreAllocGrp', 'Parties',
                                 'QuodTradeQualifier', 'BookID', 'SettlCurrency', 'TradeReportingIndicator', 'LastMkt',
                                 'Text', 'GatingRuleCondName', 'GatingRuleName', 'PartyRoleQualifier']
        exec_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_new(self.fix_message).change_parameters(
            {"NoParty": parties, "Currency": self.cur})
        exec_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_filled(
            self.fix_message).change_parameters(
            {"NoParty": parties, "Account": self.client,
             "Currency": self.cur})
        # endregion
        # region Check ExecutionReports
        self.fix_verifier_dc.check_fix_message_fix_standard(exec_report1, ignored_fields=ignor_list_new_ord)
        self.fix_verifier_dc.check_fix_message_fix_standard(exec_report2, ignored_fields=ignor_list_filled_ord)
        # endregion
        # region check alloc instr report
        parties = {
            'NoParty': [self.data_set.get_counterpart_id_fix('counterpart_id_investment_firm_cl_counterpart'),
                        self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
                        self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user_2'),
                        self.data_set.get_counterpart_id_fix('counterpart_id_euro_clear')
                        ]
        }
        alloc_list_ignor = ['AvgPx', 'Currency', 'tag5120', 'RootOrClientCommission', 'RootOrClientCommissionCurrency',
                            'NoRootMiscFeesList', 'RootCommTypeClCommBasis', 'Account', 'OrderAvgPx',
                            'PartyRoleQualifier', 'ExecAllocGrp']
        alloc_report = FixMessageAllocationInstructionReportOMS().set_default_ready_to_book(self.fix_message)
        alloc_report.change_parameters({'NoParty': parties})
        self.fix_verifier_dc.check_fix_message_fix_standard(alloc_report, ignored_fields=alloc_list_ignor)
        # endregion
        # region Set-up parameters Confirmation report
        parties = {
            'NoParty': [self.data_set.get_counterpart_id_fix('counterpart_id_investment_firm_cl_counterpart_sa3'),
                        self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
                        self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user_2'),
                        self.data_set.get_counterpart_id_fix('counterpart_id_euro_clear')
                        ]
        }
        conf_list_ignor = ['AvgPx', 'Currency', 'tag5120', 'RootOrClientCommission', 'RootOrClientCommissionCurrency',
                           'NoRootMiscFeesList', 'RootCommTypeClCommBasis', 'Account', 'NoMiscFees', 'CommissionData',
                           'OrderAvgPx', 'tag11245', 'PartyRoleQualifier']
        conf_report = FixMessageConfirmationReportOMS(self.data_set).set_default_confirmation_new(
            self.fix_message)
        conf_report.change_parameters({'NoParty': parties})
        # endregion
        # region Confirmation report
        self.fix_verifier_dc.check_fix_message_fix_standard(conf_report, ignored_fields=conf_list_ignor)
        # endregion
