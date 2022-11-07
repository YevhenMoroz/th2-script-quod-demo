import logging
import time
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
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
class QAP_T7473(TestCase):
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
                                      'AllocQty': "100"}]}, }
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit("instrument_3")
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.fix_message.change_parameters(self.change_params)
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_counterpart_1_venue_2")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region DMA order
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            trade_rele = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.mic, int(self.price),
                                                                                            int(self.qty), 2)

            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rele)
        # endregion
        # region Set-up parameters for ExecutionReports
        parties = {
            'NoPartyIDs': [
                self.data_set.get_counterpart_id_fix('counterpart_id_investment_firm_cl_counterpart_sa3'),
                self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user_2'),
                self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
                self.data_set.get_counterpart_id_fix('counterpart_id_gtwquod4')
            ]
        }
        exec_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_new(self.fix_message).change_parameters(
            {"Parties": parties, "ReplyReceivedTime": "*", "SecondaryOrderID": "*", "LastMkt": "*", "Text": "*", "Currency": self.cur})
        exec_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_filled(
            self.fix_message).change_parameters(
            {"Parties": parties, "ReplyReceivedTime": "*", "SecondaryOrderID": "*", "LastMkt": "*", "Text": "*", "Account":self.account, "Currency": self.cur})
        exec_report2.remove_parameter("SettlCurrency")
        # endregion
        # region Check ExecutionReports
        list_ignored_fields = ['Account', 'NoMiscFees',
                               'CommissionData', 'MiscFeesGrp']
        self.fix_verifier.check_fix_message_fix_standard(exec_report1, ignored_fields=list_ignored_fields)
        self.fix_verifier.check_fix_message_fix_standard(exec_report2, ignored_fields=list_ignored_fields)
        # endregion
        # region Set-up parameters Confirmation report
        party_stub_dict = {'PartyRole': "*",
                           'PartyRoleQualifier':'*',
                           'PartyID': "*",
                           'PartyIDSource': "*"}
        no_party = {
            'NoParty': [
                self.data_set.get_counterpart_id_fix('counterpart_id_investment_firm_cl_counterpart_sa3'),
                self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
                self.data_set.get_counterpart_id_fix('counterpart_id_euro_clear'),
                party_stub_dict
            ]
        }
        conf_report = FixMessageConfirmationReportOMS(self.data_set).set_default_confirmation_new(
            self.fix_message).change_parameters(
            {"NoParty": no_party, "Account": self.client, "tag5120": "*", "AllocAccount": self.account, "Currency": self.cur_for_check, "AvgPx": "*"})
        # endregion
        # region Check Book & Allocation
        self.fix_verifier_dc.check_fix_message_fix_standard(conf_report, ignored_fields=list_ignored_fields)
        # endregion
